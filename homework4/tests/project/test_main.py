import pytest
from flask import get_flashed_messages, url_for

from config import TextData
from database.status import Status
from project import create_app


def test_index_money_empty(database_views_get_user_money, database_views_get_currencies):
    database_views_get_user_money.return_value = ''
    database_views_get_currencies.return_value = []
    with create_app().test_client() as test_client:
        test_client.set_cookie('/', 'username', 'username')
        response = test_client.get('/')
        flashed_messages = get_flashed_messages()
        assert len(flashed_messages) == 1
        assert flashed_messages[0] == TextData.GET_MONEY_ERROR
        database_views_get_user_money.assert_called_once_with(
            'username'
        )
        database_views_get_currencies.assert_called_once()
        assert response.status_code == 200


def test_index(database_views_get_user_money, database_views_get_currencies):
    database_views_get_user_money.return_value = '1000.0'
    database_views_get_currencies.return_value = []
    with create_app().test_client() as test_client:
        test_client.set_cookie('/', 'username', 'username')
        response = test_client.get('/')
        flashed_messages = get_flashed_messages()
        assert len(flashed_messages) == 0
        database_views_get_user_money.assert_called_once_with(
            'username'
        )
        database_views_get_currencies.assert_called_once()
        assert response.status_code == 200


def test_balance_money_empty(database_views_get_user_money, database_views_get_user_currencies):
    database_views_get_user_money.return_value = ''
    database_views_get_user_currencies.return_value = []
    with create_app().test_client() as test_client:
        test_client.set_cookie('/balance', 'username', 'username')
        response = test_client.get('/balance')
        flashed_messages = get_flashed_messages()
        assert len(flashed_messages) == 1
        assert flashed_messages[0] == TextData.GET_MONEY_ERROR
        database_views_get_user_money.assert_called_once_with(
            'username'
        )
        database_views_get_user_currencies.assert_called_once_with(
            'username'
        )
        assert response.status_code == 200


def test_balance(database_views_get_user_money, database_views_get_user_currencies):
    database_views_get_user_money.return_value = '1000.0'
    database_views_get_user_currencies.return_value = []
    with create_app().test_client() as test_client:
        test_client.set_cookie('/balance', 'username', 'username')
        response = test_client.get('/balance')
        flashed_messages = get_flashed_messages()
        assert len(flashed_messages) == 0
        database_views_get_user_money.assert_called_once_with(
            'username'
        )
        database_views_get_user_currencies.assert_called_once_with(
            'username'
        )
        assert response.status_code == 200


def test_history(database_views_get_operations):
    database_views_get_operations.return_value = []
    with create_app().test_client() as test_client:
        test_client.set_cookie('/history', 'username', 'username')
        response = test_client.get('/history')
        flashed_messages = get_flashed_messages()
        assert len(flashed_messages) == 0
        database_views_get_operations.assert_called_once_with(
            'username'
        )
        assert response.status_code == 200


def assert_302(response, url_to_redirect, flash_text):
    flashed_messages = get_flashed_messages()
    assert len(flashed_messages) == 1
    assert flashed_messages[0] == flash_text
    assert response.status_code == 302
    assert response.headers.get('Location') is not None
    assert response.headers.get('Location') == url_to_redirect


def func_test_buy_or_sell_some_none(route, url_to_redirect_name):
    assert route in ['/buy', '/sell']

    # rate none
    with create_app().test_client() as test_client:
        test_client.set_cookie(route, 'username', 'username')
        response = test_client.post(route, data={'name': 'name', 'count': 'count'})
        url_to_redirect = url_for(url_to_redirect_name)
        assert_302(response, url_to_redirect, TextData.SMTH_ERROR)

    # count none
    with create_app().test_client() as test_client:
        test_client.set_cookie(route, 'username', 'username')
        response = test_client.post(route, data={'name': 'name', 'rate': 'rate'})
        url_to_redirect = url_for(url_to_redirect_name)
        assert_302(response, url_to_redirect, TextData.SMTH_ERROR)

    # name none
    with create_app().test_client() as test_client:
        test_client.set_cookie(route, 'username', 'username')
        response = test_client.post(route, data={'rate': 'rate', 'count': 'count'})
        url_to_redirect = url_for(url_to_redirect_name)
        assert_302(response, url_to_redirect, TextData.SMTH_ERROR)


def test_buy_or_sell_some_none():
    func_test_buy_or_sell_some_none('/buy', 'main.index')
    func_test_buy_or_sell_some_none('/sell', 'main.balance')


def func_test_buy_or_sell_count_not_num(route, url_to_redirect_name):
    assert route in ['/buy', '/sell']

    # not num
    with create_app().test_client() as test_client:
        test_client.set_cookie(route, 'username', 'username')
        response = test_client.post(route, data={'name': 'name', 'count': 'count', 'rate': 'rate'})
        url_to_redirect = url_for(url_to_redirect_name)
        assert_302(response, url_to_redirect, TextData.COUNT_NOT_NUM)

    # empty
    with create_app().test_client() as test_client:
        test_client.set_cookie(route, 'username', 'username')
        response = test_client.post(route, data={'name': 'name', 'count': '', 'rate': 'rate'})
        url_to_redirect = url_for(url_to_redirect_name)
        assert_302(response, url_to_redirect, TextData.COUNT_NOT_NUM)

    # zero
    with create_app().test_client() as test_client:
        test_client.set_cookie(route, 'username', 'username')
        response = test_client.post(route, data={'name': 'name', 'count': '0', 'rate': 'rate'})
        url_to_redirect = url_for(url_to_redirect_name)
        assert_302(response, url_to_redirect, TextData.COUNT_NOT_NUM)


def test_buy_or_sell_count_not_num():
    func_test_buy_or_sell_count_not_num('/buy', 'main.index')
    func_test_buy_or_sell_count_not_num('/sell', 'main.balance')


def func_test_buy_or_sell(route, url_to_redirect_name, mock_func, msg):
    assert route in ['/buy', '/sell']

    with create_app().test_client() as test_client:
        test_client.set_cookie(route, 'username', 'username')
        response = test_client.post(route, data={'name': 'name', 'count': '1', 'rate': '1'})
        url_to_redirect = url_for(url_to_redirect_name)
        assert_302(response, url_to_redirect, msg)
        mock_func.assert_called_once_with(
            'username', 'name', '1.0', '1'
        )


@pytest.mark.parametrize(('status', 'msg'), [
    (Status.TIME_EXP, TextData.RATE_UPDATED),
    (Status.NO_MONEY, TextData.NO_ENOUGH_MONEY),
    (Status.ERROR, TextData.SMTH_ERROR),
    (Status.OK, TextData.OPERATION_OK),
])
def test_buy_or_sell(database_views_buy, database_views_sell, status, msg):
    database_views_buy.return_value = status
    database_views_sell.return_value = status
    database_views_buy.__name__ = 'database_views_buy'
    database_views_sell.__name__ = 'database_views_sell'
    func_test_buy_or_sell('/buy', 'main.index', database_views_buy, msg)
    func_test_buy_or_sell('/sell', 'main.balance', database_views_sell, msg)
