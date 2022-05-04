from fastapi.security import HTTPBasicCredentials
from fastapi.testclient import TestClient

from app.__main__ import app
from app.utils.auth import make_base64_string
from database.schemas import User

from ...static import user_proxy_data


def test_users_get_no_user(prepare_db_env, test_headers_user_1):
    _, data = user_proxy_data()[0]
    client = TestClient(app)
    response = client.get(
        '/users',
        headers=test_headers_user_1,
    )
    assert response.status_code == 401


def test_users_get_wrong_password(prepare_db_user_env):
    _, data = user_proxy_data()[0]
    cred = HTTPBasicCredentials(username=data['username'], password='wrong')
    client = TestClient(app)
    response = client.get(
        '/users',
        headers={
            'Authorization': f'Basic {make_base64_string(**cred.dict())}'
        },
    )
    assert response.status_code == 401


def test_users_get(prepare_db_user_env, test_headers_user_1):
    model, data = user_proxy_data()[0]
    client = TestClient(app)
    response = client.get(
        '/users',
        headers=test_headers_user_1,
    )
    assert response.status_code == 200
    assert response.json() == User(username=data['username']).dict()


def test_users_post_exists(prepare_db_user_env, test_headers_user_1):
    client = TestClient(app)
    response = client.post(
        '/users',
        headers=test_headers_user_1,
    )
    assert response.status_code == 307
    response = client.send(response.next)
    assert response.status_code == 409


def test_users_post(prepare_db_env, test_headers_user_1):
    model, data = user_proxy_data()[0]
    client = TestClient(app)
    response = client.post(
        '/users',
        headers=test_headers_user_1,
    )
    assert response.status_code == 307
    response = client.send(response.next)
    assert response.status_code == 200
    assert response.json() == User(username=data['username']).dict()
