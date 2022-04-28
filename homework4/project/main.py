import logging
from typing import Any, Callable

from flask import Blueprint, flash, redirect, render_template, request, url_for

import database.views
from database.status import Status as DatabaseStatus
from database.utils import normalize_money_str
from project.utils import login_required

from config import TextData

bp_main = Blueprint('main', __name__)
logger = logging.getLogger(__name__)


@bp_main.route('/')
@login_required
def index(username: str) -> Any:
    money = database.views.get_user_money(username)
    if money == '':
        flash(TextData.GET_MONEY_ERROR)
        logger.info('Error in database.views.get_user_money')
    currencies = database.views.get_currencies()

    return render_template(
        'index.html', login=username, money=money, currencies=currencies
    )


@bp_main.route('/balance')
@login_required
def balance(username: str) -> Any:
    money = database.views.get_user_money(username)
    if money == '':
        flash(TextData.GET_MONEY_ERROR)
        logger.info('Error in database.views.get_user_money')
    currencies = database.views.get_user_currencies(username)

    return render_template(
        'balance.html', login=username, money=money, currencies=currencies
    )


@bp_main.route('/history')
@login_required
def history(username: str) -> Any:
    all_operations = database.views.get_operations(username)
    return render_template(
        'history.html', login=username, all_operations=all_operations
    )


def buy_or_sell(
    username: str,
    op_func: Callable[[str, str, str, str], DatabaseStatus],
    url_for_redirect: str,
) -> Any:
    currency_name = request.form.get('name')
    count_str_not_norm = request.form.get('count')
    rate_str = request.form.get('rate')
    if count_str_not_norm is None or currency_name is None or rate_str is None:
        flash(TextData.SMTH_ERROR)
        logger.info('Error in form: %s', request.form)
        return redirect(url_for_redirect)
    count_str = normalize_money_str(count_str_not_norm)
    if count_str == '' or count_str == '0.0':
        flash(TextData.COUNT_NOT_NUM)
        logger.info('Error in count_str: %s', count_str)
        return redirect(url_for_redirect)
    count_list = count_str.split('.')

    if (
        len(count_list) == 2
        and count_list[0].isnumeric()
        and count_list[1].isnumeric()
        or len(count_list) == 1
        and count_list[0].isnumeric()
    ):
        logger.info(
            '%s for %s: %s %s',
            op_func.__name__,
            username,
            count_str,
            currency_name,
        )
        db_status = op_func(username, currency_name, count_str, rate_str)
        if db_status:
            logger.info('database.views.buy exit with %s', db_status)
            if db_status == DatabaseStatus.TIME_EXP:
                flash(TextData.RATE_UPDATED)
            elif db_status == DatabaseStatus.NO_MONEY:
                flash(TextData.NO_ENOUGH_MONEY)
            else:
                flash(TextData.SMTH_ERROR)
        else:
            flash(TextData.OPERATION_OK)
    else:
        flash(TextData.COUNT_NOT_NUM)
    return redirect(url_for_redirect)


@bp_main.route('/buy', methods=['POST'])
@login_required
def buy(username: str) -> Any:
    return buy_or_sell(username, database.views.buy, url_for('main.index'))


@bp_main.route('/sell', methods=['POST'])
@login_required
def sell(username: str) -> Any:
    return buy_or_sell(username, database.views.sell, url_for('main.balance'))
