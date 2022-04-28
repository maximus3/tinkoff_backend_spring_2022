import datetime as dt
import logging
import random
from typing import Any, Optional

from sqlalchemy.orm import Session

from config import cfg

from . import create_session
from .models import Currency, Operation, User, UserCurrency
from .proxy import BuySellModelsProxy, CurrencyProxy, OperationProxy
from .status import Status
from .utils import op_str_add, op_str_mul, op_str_sub, str_to_money_tuple

logger = logging.getLogger(__name__)


def get_money_cur(session: Session) -> Optional[Currency]:
    return session.query(Currency).filter_by(name=cfg.money_name).first()


def create_or_exists_user(login: str) -> tuple[Status, str]:
    with create_session() as session:
        user = session.query(User).filter_by(login=login).first()
        if user:
            return Status.EXISTS, login
        created_at = dt.datetime.now()
        new_user = User(
            created_at=created_at, updated_at=created_at, login=login
        )
        session.add(new_user)
        currency = get_money_cur(session)
        if currency is None:
            logger.error('currency is None')
            return Status.ERROR, ''
        user_currency = UserCurrency(
            created_at=created_at,
            updated_at=created_at,
            user_id=new_user.id,
            currency_id=currency.id,
            count=cfg.default_money,
        )
        session.add(user_currency)
        return Status.OK, login


def get_user_money(login: str) -> str:
    with create_session() as session:
        user = session.query(User).filter_by(login=login).first()
        if user is None:
            logger.error('user is None')
            return ''
        currency = get_money_cur(session)
        if currency is None:
            logger.error('currency is None')
            return ''
        user_currency = (
            session.query(UserCurrency)
            .filter_by(user_id=user.id, currency_id=currency.id)
            .first()
        )
        return user_currency.count


def get_user_currencies(login: str) -> list[CurrencyProxy]:
    with create_session() as session:
        data = []
        user = session.query(User).filter_by(login=login).first()
        user_currencies = (
            session.query(UserCurrency).filter_by(user_id=user.id).all()
        )
        for user_currency in user_currencies:
            currency = (
                session.query(Currency)
                .filter_by(id=user_currency.currency_id)
                .first()
            )
            if currency.name == cfg.money_name:
                continue
            data.append(
                CurrencyProxy(
                    currency.name, currency.rate, user_currency.count
                )
            )
        return data


def get_operations(login: str) -> list[OperationProxy]:
    with create_session() as session:
        data = []
        user = session.query(User).filter_by(login=login).first()
        operations = session.query(Operation).filter_by(user_id=user.id).all()
        for operation in operations:
            currency = (
                session.query(Currency)
                .filter_by(id=operation.currency_id)
                .first()
            )
            data.append(OperationProxy(operation, currency.name))
        return data


def get_currencies() -> list[CurrencyProxy]:
    with create_session() as session:
        data = []
        for currency in session.query(Currency).all():
            if currency.name == cfg.money_name:
                continue
            data.append(CurrencyProxy(currency.name, currency.rate))
        return data


def currency_is_enough(
    session: Session, user: User, currency: Currency, need_value: str
) -> bool:
    user_currency = (
        session.query(UserCurrency)
        .filter_by(user_id=user.id, currency_id=currency.id)
        .first()
    )
    if user_currency is None:
        return False
    currency_count = user_currency.count
    if str_to_money_tuple(currency_count) < str_to_money_tuple(need_value):
        return False
    return True


def get_buy_sell_data(
    session: Session, login: str, currency_name: str
) -> Optional[BuySellModelsProxy]:
    user = session.query(User).filter_by(login=login).first()
    money_currency = get_money_cur(session)
    if money_currency is None:
        logger.error('currency is None')
        return None
    money_user_currency = (
        session.query(UserCurrency)
        .filter_by(user_id=user.id, currency_id=money_currency.id)
        .first()
    )
    currency = session.query(Currency).filter_by(name=currency_name).first()
    user_currency = (
        session.query(UserCurrency)
        .filter_by(user_id=user.id, currency_id=currency.id)
        .first()
    )
    return BuySellModelsProxy(
        user, money_currency, money_user_currency, currency, user_currency
    )


def check_buy_sell_restr(
    session: Session,
    currency: Currency,
    user: User,
    money_currency: Currency,
    was_rate: str,
    count_str: str,
    is_buy: bool,
) -> tuple[Status, str]:
    cur_rate = currency.rate
    if cur_rate != was_rate:
        return Status.TIME_EXP, ''
    if count_str == '0.0':
        return Status.COUNT_IS_ZERO, ''
    money_for_balance = op_str_mul(count_str, cur_rate)
    if is_buy and not currency_is_enough(
        session, user, money_currency, money_for_balance
    ):
        return Status.NO_MONEY, ''
    if not is_buy and not currency_is_enough(
        session, user, currency, count_str
    ):
        return Status.NO_MONEY, ''
    return Status.OK, money_for_balance


def buy_or_sell(
    op_type: str, login: str, currency_name: str, count_str: str, was_rate: str
) -> Status:
    is_buy = op_type == 'BUY'
    with create_session() as session:
        models_proxy = get_buy_sell_data(session, login, currency_name)
        if models_proxy is None:
            return Status.ERROR
        status_restr, money_for_balance = check_buy_sell_restr(
            session,
            models_proxy.currency,
            models_proxy.user,
            models_proxy.money_currency,
            was_rate,
            count_str,
            is_buy,
        )
        if status_restr:
            return status_restr
        created_at = dt.datetime.now()

        operation = Operation(
            created_at=created_at,
            updated_at=created_at,
            user_id=models_proxy.user.id,
            currency_id=models_proxy.currency.id,
            type=op_type,
            count=count_str,
            rate=was_rate,
            money=money_for_balance,
        )
        session.add(operation)

        if is_buy:
            if models_proxy.user_currency:
                user_currency = models_proxy.user_currency
                new_count = op_str_add(
                    user_currency.count, count_str
                )
                user_currency.updated_at = created_at
                user_currency.count = new_count
            else:
                user_currency = UserCurrency(
                    created_at=created_at,
                    updated_at=created_at,
                    user_id=models_proxy.user.id,
                    currency_id=models_proxy.currency.id,
                    count=count_str,
                )
            session.add(user_currency)
        else:
            new_count = op_str_sub(models_proxy.user_currency.count, count_str)
            if str_to_money_tuple(new_count) == (0, 0):
                session.query(UserCurrency).filter_by(
                    user_id=models_proxy.user.id,
                    currency_id=models_proxy.currency.id,
                ).delete()
            else:
                models_proxy.user_currency.updated_at = created_at
                models_proxy.user_currency.count = new_count
                session.add(models_proxy.user_currency)

        if is_buy:
            new_balance = op_str_sub(
                models_proxy.money_user_currency.count, money_for_balance
            )
        else:
            new_balance = op_str_add(
                models_proxy.money_user_currency.count, money_for_balance
            )
        models_proxy.money_user_currency.count = new_balance
        session.add(models_proxy.money_user_currency)
        return Status.OK


def buy(*args: Any, **kwargs: Any) -> Status:
    return buy_or_sell('BUY', *args, **kwargs)


def sell(*args: Any, **kwargs: Any) -> Status:
    return buy_or_sell('SELL', *args, **kwargs)


def update_rates() -> None:
    with create_session() as session:
        for currency in session.query(Currency).all():
            if currency.name == cfg.money_name:
                continue
            rate_mult = random.randint(0, 10)
            rate_perc = op_str_mul(currency.rate, '0.' + str(rate_mult))
            if random.random() > 0.5:
                currency.rate = op_str_add(currency.rate, rate_perc)
            else:
                currency.rate = op_str_sub(currency.rate, rate_perc)
            session.add(currency)
        logger.info('Currencies rates updated')
