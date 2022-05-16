import pytest
from flask import get_flashed_messages, url_for

from config.text import TextData


@pytest.mark.usefixtures('user_logged_in')
def test_login_get_already(test_client):
    response = test_client.get('/login')
    flashed_messages = get_flashed_messages()
    assert len(flashed_messages) == 1
    assert flashed_messages[0] == TextData.ALREADY_LOGGED
    assert response.status_code == 302
    assert response.headers.get('Location') == url_for('main.index')


def test_login_get(test_client):
    response = test_client.get('/login')
    assert response.status_code == 200


def test_logout_not_logged(test_client):
    response = test_client.get('/logout')
    flashed_messages = get_flashed_messages()
    assert len(flashed_messages) == 1
    assert flashed_messages[0] == TextData.LOGIN_REQU
    assert response.status_code == 302
    assert response.headers.get('Location') == url_for('auth.login')


@pytest.mark.usefixtures('user_logged_in')
def test_logout(test_client):
    response = test_client.get('/logout')
    assert response.status_code == 302
    assert response.headers.get('Location') is not None
    assert response.headers.get('Location') == url_for(
        'auth.login'
    )  # TODO: all?


@pytest.mark.usefixtures('user_logged_in')
def test_login_post_already_logged(test_client):
    response = test_client.post('/login')
    flashed_messages = get_flashed_messages()
    assert len(flashed_messages) == 1
    assert flashed_messages[0] == TextData.ALREADY_LOGGED
    assert response.status_code == 302
    assert response.headers.get('Location') == url_for('main.index')


def test_login_post(test_client, prepare_db_user_env):
    response = test_client.post(
        '/login', data={'login': 'username', 'password': 'password'}
    )
    flashed_messages = get_flashed_messages()
    assert len(flashed_messages) == 0
    assert response.status_code == 302
    assert response.headers.get('Location') is not None
    assert response.headers.get('Location') == url_for('main.index')


def test_login_post_no_username(test_client, prepare_db_user_env):
    response = test_client.post(
        '/login', data={'login': '1', 'password': 'password'}
    )
    flashed_messages = get_flashed_messages()
    assert len(flashed_messages) == 1
    assert flashed_messages[0] == TextData.LOGIN_FAILED
    assert response.status_code == 302
    assert response.headers.get('Location') is not None
    assert response.headers.get('Location') == url_for('auth.login')


def test_login_post_none_username(test_client, prepare_db_user_env):
    response = test_client.post('/login', data={'password': 'password'})
    flashed_messages = get_flashed_messages()
    assert len(flashed_messages) == 1
    assert flashed_messages[0] == TextData.SMTH_ERROR
    assert response.status_code == 302
    assert response.headers.get('Location') is not None
    assert response.headers.get('Location') == url_for('auth.login')


def test_login_post_none_password(test_client, prepare_db_user_env):
    response = test_client.post('/login', data={'login': 'username'})
    flashed_messages = get_flashed_messages()
    assert len(flashed_messages) == 1
    assert flashed_messages[0] == TextData.SMTH_ERROR
    assert response.status_code == 302
    assert response.headers.get('Location') is not None
    assert response.headers.get('Location') == url_for('auth.login')


def test_login_post_wrong_password(test_client, prepare_db_user_env):
    response = test_client.post(
        '/login', data={'login': 'username', 'password': '1'}
    )
    flashed_messages = get_flashed_messages()
    assert len(flashed_messages) == 1
    assert flashed_messages[0] == TextData.LOGIN_FAILED
    assert response.status_code == 302
    assert response.headers.get('Location') is not None
    assert response.headers.get('Location') == url_for('auth.login')


def test_login_post_none(test_client):
    response = test_client.post('/login')
    flashed_messages = get_flashed_messages()
    assert len(flashed_messages) == 1
    assert flashed_messages[0] == TextData.SMTH_ERROR
    assert response.status_code == 302
    assert response.headers.get('Location') == url_for('auth.login')


@pytest.mark.usefixtures('user_logged_in')
def test_signup_get_already(test_client):
    response = test_client.get('/signup')
    flashed_messages = get_flashed_messages()
    assert len(flashed_messages) == 1
    assert flashed_messages[0] == TextData.ALREADY_LOGGED
    assert response.status_code == 302
    assert response.headers.get('Location') == url_for('main.index')


def test_signup_get(test_client):
    response = test_client.get('/signup')
    assert response.status_code == 200


def test_signup_post_exists(test_client, prepare_db_user_env):
    response = test_client.post(
        '/signup', data={'login': 'username', 'password': 'password'}
    )
    flashed_messages = get_flashed_messages()
    assert len(flashed_messages) == 1
    assert flashed_messages[0] == TextData.USER_EXISTS
    assert response.status_code == 302
    assert response.headers.get('Location') is not None
    assert response.headers.get('Location') == url_for('auth.signup')


@pytest.mark.usefixtures('user_logged_in')
def test_signup_post_already_logged(test_client):
    response = test_client.post('/signup')
    flashed_messages = get_flashed_messages()
    assert len(flashed_messages) == 1
    assert flashed_messages[0] == TextData.ALREADY_LOGGED
    assert response.status_code == 302
    assert response.headers.get('Location') == url_for('main.index')


def test_signup_post(test_client, prepare_db_env):
    response = test_client.post(
        '/signup', data={'login': 'username', 'password': 'password'}
    )
    flashed_messages = get_flashed_messages()
    assert len(flashed_messages) == 0
    assert response.status_code == 302
    assert response.headers.get('Location') is not None
    assert response.headers.get('Location') == url_for('auth.login')


def test_signup_post_none_username(test_client, prepare_db_env):
    response = test_client.post('/signup', data={'password': 'password'})
    flashed_messages = get_flashed_messages()
    assert len(flashed_messages) == 1
    assert flashed_messages[0] == TextData.SMTH_ERROR
    assert response.status_code == 302
    assert response.headers.get('Location') is not None
    assert response.headers.get('Location') == url_for('auth.signup')


def test_signup_post_none_password(test_client, prepare_db_env):
    response = test_client.post('/signup', data={'login': 'username'})
    flashed_messages = get_flashed_messages()
    assert len(flashed_messages) == 1
    assert flashed_messages[0] == TextData.SMTH_ERROR
    assert response.status_code == 302
    assert response.headers.get('Location') is not None
    assert response.headers.get('Location') == url_for('auth.signup')


def test_signup_post_none(test_client):
    response = test_client.post('/signup')
    flashed_messages = get_flashed_messages()
    assert len(flashed_messages) == 1
    assert flashed_messages[0] == TextData.SMTH_ERROR
    assert response.status_code == 302
    assert response.headers.get('Location') == url_for('auth.signup')
