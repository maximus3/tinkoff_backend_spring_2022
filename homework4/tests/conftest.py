import pytest

from .database.config import prepare_db, remove_db, Session
from .database import tmp_database_name

import database.views


@pytest.fixture()
def database_views_create_or_exists_user_mock(mocker):
    return mocker.patch('database.views.create_or_exists_user')


@pytest.fixture()
def database_views_get_user_money(mocker):
    return mocker.patch('database.views.get_user_money')


@pytest.fixture()
def database_views_get_currencies(mocker):
    return mocker.patch('database.views.get_currencies')


@pytest.fixture()
def database_views_get_user_currencies(mocker):
    return mocker.patch('database.views.get_user_currencies')


@pytest.fixture()
def database_views_get_operations(mocker):
    return mocker.patch('database.views.get_operations')


@pytest.fixture()
def database_views_buy(mocker):
    return mocker.patch('database.views.buy')


@pytest.fixture()
def database_views_sell(mocker):
    return mocker.patch('database.views.sell')


@pytest.fixture()
def prepare_db_env(mocker):
    mocker.patch('database.Session', Session)
    mocker.patch('config.cfg.DATABASE_FILENAME', tmp_database_name)
    mocker.patch('config.cfg.DATABASE_ENGINE', 'sqlite:///' + tmp_database_name)
    prepare_db()
    yield
    remove_db()


@pytest.fixture()
def prepare_db_env_with_user(prepare_db_env):
    database.views.create_or_exists_user('login')
    yield


@pytest.fixture()
def database_views_get_money_cur(mocker):
    return mocker.patch('database.views.get_money_cur')
