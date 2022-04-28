import datetime as dt

import pytest

from config import cfg
from database.models import UserCurrency, Currency, User, Operation
from database.proxy import CurrencyProxy, OperationProxy, BuySellModelsProxy

from . import tmp_database_name
from .config import create_session
from database.status import Status
import database.views


def test_get_money_cur(prepare_db_env):
    with create_session() as session:
        assert str(session.get_bind().url) == 'sqlite:///' + tmp_database_name
        currency = database.views.get_money_cur(session)
        assert currency is not None
        assert currency.name == cfg.money_name


def test_create_or_exists_user_ok(prepare_db_env):
    result = database.views.create_or_exists_user('login')
    assert result == (Status.OK, 'login')


def test_create_or_exists_user_exists(prepare_db_env_with_user):
    result = database.views.create_or_exists_user('login')
    assert result == (Status.EXISTS, 'login')


def test_create_or_exists_user_err(prepare_db_env, database_views_get_money_cur):
    database_views_get_money_cur.return_value = None
    result = database.views.create_or_exists_user('login')
    assert result == (Status.ERROR, '')


def test_get_user_money(prepare_db_env_with_user):
    result = database.views.get_user_money('login')
    assert result == cfg.default_money


def test_get_user_money_no_such_user(prepare_db_env):
    result = database.views.get_user_money('login')
    assert result == ''


def test_get_user_money_err(prepare_db_env_with_user, database_views_get_money_cur):
    database_views_get_money_cur.return_value = None
    result = database.views.get_user_money('login')
    assert result == ''


def test_get_user_currencies(prepare_db_env_with_user):
    result = database.views.get_user_currencies('login')
    assert result == []


def test_get_user_currencies_some_add(prepare_db_env_with_user):
    with create_session() as session:
        money_currency = database.views.get_money_cur(session)
        currency = session.query(Currency).filter(Currency.id != money_currency.id).first()
        user = session.query(User).filter_by(login='login').one()
        created_at = dt.datetime.now()
        user_currency = UserCurrency(
            created_at=created_at,
            updated_at=created_at,
            user_id=user.id,
            currency_id=currency.id,
            count='100.0',
        )
        session.add(user_currency)
        currency_proxy = CurrencyProxy(currency.name, currency.rate, user_currency.count)
    result = database.views.get_user_currencies('login')
    assert result == [currency_proxy]
    return currency_proxy


def test_get_operations(prepare_db_env_with_user):
    result = database.views.get_operations('login')
    assert result == []


def test_get_operations_some_add(prepare_db_env_with_user):
    with create_session() as session:
        money_currency = database.views.get_money_cur(session)
        currency = session.query(Currency).filter(Currency.id != money_currency.id).first()
        user = session.query(User).filter_by(login='login').one()
        created_at = dt.datetime.now()

        operation = Operation(
            created_at=created_at,
            updated_at=created_at,
            user_id=user.id,
            currency_id=currency.id,
            type='BUY',
            count='100.0',
            rate='1.0',
            money='100.0',
        )

        session.add(operation)
        operation_proxy = OperationProxy(operation, currency.name)
    result = database.views.get_operations('login')
    assert result == [operation_proxy]


def test_get_currencies(prepare_db_env_with_user):
    result = database.views.get_currencies()
    assert len(result) == 5


def test_currency_is_enough_no_such_cur(prepare_db_env_with_user):
    with create_session() as session:
        money_currency = database.views.get_money_cur(session)
        currency = session.query(Currency).filter(Currency.id != money_currency.id).first()
        user = session.query(User).filter_by(login='login').one()
        assert not database.views.currency_is_enough(session, user, currency, '1.0')


def test_currency_is_enough_no(prepare_db_env_with_user):
    with create_session() as session:
        money_currency = database.views.get_money_cur(session)
        user = session.query(User).filter_by(login='login').one()
        assert not database.views.currency_is_enough(session, user, money_currency, '10000.0')


def test_currency_is_enough_yes_edge(prepare_db_env_with_user):
    with create_session() as session:
        money_currency = database.views.get_money_cur(session)
        user = session.query(User).filter_by(login='login').one()
        assert database.views.currency_is_enough(session, user, money_currency, '1000.0')


def test_currency_is_enough_yes(prepare_db_env_with_user):
    with create_session() as session:
        money_currency = database.views.get_money_cur(session)
        user = session.query(User).filter_by(login='login').one()
        assert database.views.currency_is_enough(session, user, money_currency, '100.0')


def test_get_buy_sell_data(prepare_db_env_with_user):
    with create_session() as session:
        money_currency = database.views.get_money_cur(session)
        currency = session.query(Currency).filter(Currency.id != money_currency.id).first()
        user = session.query(User).filter_by(login='login').one()
        money_user_currency = (
            session.query(UserCurrency)
                .filter_by(user_id=user.id, currency_id=money_currency.id)
                .first()
        )
        user_currency = (
            session.query(UserCurrency)
                .filter_by(user_id=user.id, currency_id=currency.id)
                .first()
        )
        need_result = BuySellModelsProxy(
            user, money_currency, money_user_currency, currency, user_currency
        )
        assert database.views.get_buy_sell_data(session, 'login', currency.name) == need_result
    return need_result


def test_get_buy_sell_data_no_money_currency(prepare_db_env_with_user, database_views_get_money_cur):
    database_views_get_money_cur.return_value = None
    with create_session() as session:
        assert database.views.get_buy_sell_data(session, 'login', 'currency_name') is None


def test_check_buy_sell_restr_rate_updated(prepare_db_env_with_user):
    # create currency
    currency_proxy = test_get_user_currencies_some_add(prepare_db_env_with_user)
    with create_session() as session:
        money_currency = database.views.get_money_cur(session)
        currency = session.query(Currency).filter(Currency.id != money_currency.id).first()
        user = session.query(User).filter_by(login='login').one()
        assert database.views.check_buy_sell_restr(session, currency, user, money_currency, currency_proxy.rate + '1',
                                                   'count_str', True) == (Status.TIME_EXP, '')


def test_check_buy_sell_restr_count_zero(prepare_db_env_with_user):
    # create currency
    currency_proxy = test_get_user_currencies_some_add(prepare_db_env_with_user)
    with create_session() as session:
        money_currency = database.views.get_money_cur(session)
        currency = session.query(Currency).filter(Currency.id != money_currency.id).first()
        user = session.query(User).filter_by(login='login').one()
        assert database.views.check_buy_sell_restr(session, currency, user, money_currency, currency_proxy.rate,
                                                   '0.0', True) == (Status.COUNT_IS_ZERO, '')


def test_check_buy_sell_restr_is_buy_and_not_enough(prepare_db_env_with_user):
    # create currency
    currency_proxy = test_get_user_currencies_some_add(prepare_db_env_with_user)
    with create_session() as session:
        money_currency = database.views.get_money_cur(session)
        currency = session.query(Currency).filter(Currency.id != money_currency.id).first()
        user = session.query(User).filter_by(login='login').one()
        assert database.views.check_buy_sell_restr(session, currency, user, money_currency, currency_proxy.rate,
                                                   '100000000.0', True) == (Status.NO_MONEY, '')


def test_check_buy_sell_restr_not_is_buy_and_not_enough(prepare_db_env_with_user):
    # create currency
    currency_proxy = test_get_user_currencies_some_add(prepare_db_env_with_user)
    with create_session() as session:
        money_currency = database.views.get_money_cur(session)
        currency = session.query(Currency).filter(Currency.id != money_currency.id).first()
        user = session.query(User).filter_by(login='login').one()
        assert database.views.check_buy_sell_restr(session, currency, user, money_currency, currency_proxy.rate,
                                                   '100000000.0', False) == (Status.NO_MONEY, '')


def test_check_buy_sell_restr_ok(prepare_db_env_with_user):
    # create currency
    currency_proxy = test_get_user_currencies_some_add(prepare_db_env_with_user)
    with create_session() as session:
        money_currency = database.views.get_money_cur(session)
        currency = session.query(Currency).filter(Currency.id != money_currency.id).first()
        user = session.query(User).filter_by(login='login').one()
        assert database.views.check_buy_sell_restr(session, currency, user, money_currency, currency_proxy.rate,
                                                   '1.0', True) == (Status.OK, currency_proxy.rate)


def test_buy_or_sell_models_proxy_none(prepare_db_env_with_user, database_views_get_money_cur):
    database_views_get_money_cur.return_value = None
    with create_session():
        assert database.views.buy('login', 'currency_name', '1.0', '1.0') == Status.ERROR
        assert database.views.sell('login', 'currency_name', '1.0', '1.0') == Status.ERROR


def test_buy_or_sell_status_restr(prepare_db_env_with_user):
    # create currency
    currency_proxy = test_get_user_currencies_some_add(prepare_db_env_with_user)
    count_str = '1000000.0'
    was_rate = currency_proxy.rate
    assert database.views.buy('login', currency_proxy.name, count_str, was_rate) == Status.NO_MONEY
    assert database.views.sell('login', currency_proxy.name, count_str, was_rate) == Status.NO_MONEY


def test_buy_or_sell_status_ok(prepare_db_env_with_user):
    currency_proxy = test_get_user_currencies_some_add(prepare_db_env_with_user)
    count_str = '1.0'
    was_rate = currency_proxy.rate
    assert database.views.buy('login', currency_proxy.name, count_str, was_rate) == Status.OK
    assert database.views.sell('login', currency_proxy.name, count_str, was_rate) == Status.OK
    assert database.views.sell('login', currency_proxy.name, currency_proxy.count, was_rate) == Status.OK


def test_update_rates(prepare_db_env):
    was_rates = []
    with create_session() as session:
        for currency in session.query(Currency).all():
            if currency.name == cfg.money_name:
                continue
            was_rates.append(currency.rate)
    database.views.update_rates()
    new_rates = []
    with create_session() as session:
        for currency in session.query(Currency).all():
            if currency.name == cfg.money_name:
                continue
            new_rates.append(currency.rate)
    assert not was_rates == new_rates
