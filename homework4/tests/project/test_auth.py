from flask import get_flashed_messages, url_for

from config import TextData
from database.status import Status
from project import create_app


def test_login_already():
    with create_app().test_client() as test_client:
        test_client.set_cookie('/login', 'username', 'username')
        response = test_client.get('/login')
        flashed_messages = get_flashed_messages()
        assert len(flashed_messages) == 1
        assert flashed_messages[0] == TextData.ALREADY_LOGGED
        assert response.status_code == 302
        assert response.headers.get('Location') == url_for('main.index')


def test_login():
    with create_app().test_client() as test_client:
        response = test_client.get('/login')
        assert response.status_code == 200


def test_logout_not_logged():
    with create_app().test_client() as test_client:
        response = test_client.get('/logout')
        flashed_messages = get_flashed_messages()
        assert len(flashed_messages) == 1
        assert flashed_messages[0] == TextData.LOGIN_REQU
        assert response.status_code == 302
        assert response.headers.get('Location') == url_for('auth.login')


def test_logout():
    with create_app().test_client() as test_client:
        test_client.set_cookie('/logout', 'username', 'username')
        response = test_client.get('/logout')
        assert response.status_code == 302
        assert response.headers.get('Location') is not None
        assert response.headers.get('Location') == url_for('auth.login')
        set_cookie = response.headers.get('Set-Cookie')
        assert set_cookie is not None
        assert set_cookie.startswith('username=;')


def test_login_post_already():
    with create_app().test_client() as test_client:
        test_client.set_cookie('/login', 'username', 'username')
        response = test_client.post('/login')
        flashed_messages = get_flashed_messages()
        assert len(flashed_messages) == 1
        assert flashed_messages[0] == TextData.ALREADY_LOGGED
        assert response.status_code == 302
        assert response.headers.get('Location') == url_for('main.index')


def test_login_post(database_views_create_or_exists_user_mock):
    database_views_create_or_exists_user_mock.return_value = (
        Status.OK,
        'login',
    )
    with create_app().test_client() as test_client:
        response = test_client.post('/login', data={'login': 'login'})
        database_views_create_or_exists_user_mock.assert_called_once_with(
            'login'
        )
        assert response.status_code == 302
        assert response.headers.get('Location') is not None
        assert response.headers.get('Location') == url_for('main.index')
        set_cookie = response.headers.get('Set-Cookie')
        assert set_cookie is not None
        assert set_cookie.startswith('username=login;')


def test_login_post_exists(database_views_create_or_exists_user_mock):
    database_views_create_or_exists_user_mock.return_value = (
        Status.EXISTS,
        'login',
    )
    with create_app().test_client() as test_client:
        response = test_client.post('/login', data={'login': 'login'})
        database_views_create_or_exists_user_mock.assert_called_once_with(
            'login'
        )
        assert response.status_code == 302
        assert response.headers.get('Location') is not None
        assert response.headers.get('Location') == url_for('main.index')
        set_cookie = response.headers.get('Set-Cookie')
        assert set_cookie is not None
        assert set_cookie.startswith('username=login;')


def test_login_post_error(database_views_create_or_exists_user_mock):
    database_views_create_or_exists_user_mock.return_value = (Status.ERROR, '')
    with create_app().test_client() as test_client:
        response = test_client.post('/login', data={'login': 'login'})
        database_views_create_or_exists_user_mock.assert_called_once_with(
            'login'
        )
        flashed_messages = get_flashed_messages()
        assert len(flashed_messages) == 1
        assert flashed_messages[0] == TextData.SMTH_ERROR
        assert response.status_code == 302
        assert response.headers.get('Location') == url_for('auth.login')


def test_login_post_none():
    with create_app().test_client() as test_client:
        response = test_client.post('/login')
        flashed_messages = get_flashed_messages()
        assert len(flashed_messages) == 1
        assert flashed_messages[0] == TextData.SMTH_ERROR
        assert response.status_code == 302
        assert response.headers.get('Location') == url_for('auth.login')
