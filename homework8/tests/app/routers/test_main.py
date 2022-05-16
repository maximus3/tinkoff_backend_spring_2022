import pytest
from flask import get_flashed_messages, url_for


def test_index_get(test_client):
    response = test_client.get('/')
    flashed_messages = get_flashed_messages()
    assert len(flashed_messages) == 0
    assert response.status_code == 302
    assert response.headers.get('Location') == url_for('auth.login')


@pytest.mark.usefixtures('user_logged_in')
def test_index_get_logged_in(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
