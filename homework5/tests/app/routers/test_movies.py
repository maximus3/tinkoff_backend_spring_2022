from fastapi.testclient import TestClient

from app.__main__ import app

from ...static import movie_proxy_data


def test_get_movies(movie_result):
    client = TestClient(app)
    response = client.get('/movies')
    assert response.status_code == 200
    assert response.json() == movie_result


def test_get_movies_top(movie_result):
    client = TestClient(app)
    response = client.get('/movies?top=2')
    assert response.status_code == 200
    assert response.json() == movie_result[:2]


def test_get_movies_year(movie_result):
    client = TestClient(app)
    response = client.get('/movies?year=2021')
    assert response.status_code == 200
    assert response.json() == list(
        filter(lambda x: x.year == 2021, movie_result)
    )


def test_get_movies_title(movie_result):
    client = TestClient(app)
    response = client.get('/movies?title=title')
    assert response.status_code == 200
    assert response.json() == list(
        filter(lambda x: 'title' in x.title, movie_result)
    )


def test_get_movies_page_1(movie_result):
    client = TestClient(app)
    response = client.get('/movies?page=1&per_page=2')
    assert response.status_code == 200
    assert response.json() == movie_result[:2]


def test_get_movies_page_2(movie_result):
    client = TestClient(app)
    response = client.get('/movies?page=2&per_page=2')
    assert response.status_code == 200
    assert response.json() == movie_result[2:4]


def test_get_movie_by_id_404(movie_result):
    client = TestClient(app)
    response = client.get('/movies/100')
    assert response.status_code == 404


def test_get_movie_by_id(movie_result):
    client = TestClient(app)
    response = client.get('/movies/1')
    assert response.status_code == 200
    assert response.json() == movie_proxy_data()[0][0].get_schema_model(id=1)
