from fastapi.testclient import TestClient

from app.__main__ import app
from tests.static import review_proxy_data


def test_get_reviews(review_result):
    client = TestClient(app)
    response = client.get('/reviews/1')
    assert response.status_code == 200
    assert response.json() == list(
        filter(lambda x: x.movie.id == 1, review_result)
    )


def test_get_reviews_none(review_result):
    client = TestClient(app)
    response = client.get('/reviews/100')
    assert response.status_code == 200
    assert response.json() == []


def test_reviews_post_no_params(review_result, test_headers_user_1):
    client = TestClient(app)
    response = client.post(
        '/reviews/1',
        headers=test_headers_user_1,
    )
    assert response.status_code == 422


def test_reviews_post_no_movie(movie_result, test_headers_user_1):
    client = TestClient(app)
    response = client.post(
        '/reviews/100',
        headers=test_headers_user_1,
        json={
            'review': 'review',
        },
    )
    assert response.status_code == 404


def test_reviews_post(movie_result, test_headers_user_1):
    client = TestClient(app)
    review_model, review_data = review_proxy_data()[0]
    user_model, user_data = review_data.pop('user_data')
    movie_model, movie_data = review_data.pop('movie_data')
    user = user_model.get(**user_data)
    movie = movie_model.get(**movie_data)
    response = client.post(
        f'/reviews/{movie.id}', headers=test_headers_user_1, json=review_data
    )
    assert response.status_code == 200
    assert (
        review_model.get(user_id=user.id, movie_id=movie.id).review
        == review_data['review']
    )
