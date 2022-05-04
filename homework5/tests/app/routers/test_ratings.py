from fastapi.testclient import TestClient

from app.__main__ import app
from database.proxy import RatingProxy
from tests.static import user_proxy_data


def test_rating_post_no_params(prepare_db_user_movie_env, test_headers_user_1):
    client = TestClient(app)
    response = client.post(
        '/ratings/1',
        headers=test_headers_user_1,
    )
    assert response.status_code == 422


def test_rating_post_no_movie(prepare_db_user_movie_env, test_headers_user_1):
    client = TestClient(app)
    response = client.post(
        '/ratings/100',
        headers=test_headers_user_1,
        json={
            'rating': 10,
        },
    )
    assert response.status_code == 404


def test_rating_post_rating_100(
    prepare_db_user_movie_env, test_headers_user_1
):
    client = TestClient(app)
    user_model, user_data = user_proxy_data()[0]
    user = user_model.get(**user_data)
    response = client.post(
        '/ratings/1',
        headers=test_headers_user_1,
        json={
            'rating': 100,
        },
    )
    assert response.status_code == 422


def test_rating_post_rating_neg(
    prepare_db_user_movie_env, test_headers_user_1
):
    client = TestClient(app)
    user_model, user_data = user_proxy_data()[0]
    user = user_model.get(**user_data)
    response = client.post(
        '/ratings/1',
        headers=test_headers_user_1,
        json={
            'rating': -1,
        },
    )
    assert response.status_code == 422


def test_rating_post(prepare_db_user_movie_env, test_headers_user_1):
    client = TestClient(app)
    user_model, user_data = user_proxy_data()[0]
    user = user_model.get(**user_data)
    response = client.post(
        '/ratings/1',
        headers=test_headers_user_1,
        json={
            'rating': 10,
        },
    )
    assert response.status_code == 200
    assert RatingProxy.get(user_id=user.id, movie_id=1).rating == 10
