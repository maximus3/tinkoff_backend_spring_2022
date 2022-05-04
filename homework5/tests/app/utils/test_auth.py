import pytest
from fastapi import HTTPException
from fastapi.security import HTTPBasicCredentials

from app.utils.auth import (
    base64_to_password,
    get_current_user,
    make_base64_string,
    register_user,
)

from ...static import user_proxy_data


def test_base64_to_password():
    assert base64_to_password('dGVzdDp0ZXN0') == 'test'


def test_base64_to_password_error():
    assert base64_to_password('test') == ''
    assert base64_to_password('dGVzdDp0ZXN0dGVzdDp0ZXN0') == ''


def test_make_base64_string():
    assert make_base64_string('test', 'test') == 'dGVzdDp0ZXN0'


def test_get_current_user_no_user(prepare_db_env):
    _, data = user_proxy_data()[0]
    cred = HTTPBasicCredentials(username=data['username'], password='password')
    with pytest.raises(HTTPException):
        get_current_user(cred)


def test_get_current_user_wrong_password(prepare_db_user_env):
    _, data = user_proxy_data()[0]
    cred = HTTPBasicCredentials(username=data['username'], password='wrong')
    with pytest.raises(HTTPException):
        get_current_user(cred)


def test_get_current_user(prepare_db_user_env):
    model, data = user_proxy_data()[0]
    cred = HTTPBasicCredentials(username=data['username'], password='password')
    user = get_current_user(cred)
    assert user == model.get(username=cred.username)


def test_register_user_exists(prepare_db_user_env):
    _, data = user_proxy_data()[0]
    cred = HTTPBasicCredentials(username=data['username'], password='any')
    with pytest.raises(HTTPException):
        register_user(cred)


def test_register_user(prepare_db_env):
    model, data = user_proxy_data()[0]
    cred = HTTPBasicCredentials(username=data['username'], password='password')
    user = register_user(cred)
    assert user == model.get(username=cred.username)
