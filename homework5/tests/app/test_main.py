from fastapi.testclient import TestClient

from app.__main__ import app


def test_root(prepare_db_env):
    client = TestClient(app)
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == []
