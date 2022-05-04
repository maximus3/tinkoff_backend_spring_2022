import pytest

from database import create_session

from .database import tmp_database_engine, tmp_database_name
from .database.config import Session, prepare_db, remove_db
from .static import movie_proxy_data, review_proxy_data, user_proxy_data


@pytest.fixture()
def prepare_db_env(mocker):
    mocker.patch('database.Session', Session)
    mocker.patch('config.cfg.DATABASE_NAME', tmp_database_name)
    mocker.patch('config.cfg.DATABASE_ENGINE', tmp_database_engine)
    prepare_db()
    yield
    remove_db()


@pytest.fixture()
def prepare_db_user_env(prepare_db_env):
    for model, data in user_proxy_data():
        model.create(**data)
    yield


@pytest.fixture()
def prepare_db_user_movie_env(prepare_db_user_env):
    for model, data in movie_proxy_data():
        model.create(**data)
    yield


@pytest.fixture()
def movie_result(prepare_db_user_movie_env):
    result = []
    for i, (proxy_class, data) in enumerate(movie_proxy_data()):
        result.append(proxy_class.get_schema_model(**data))
    result = sorted(result, key=lambda x: x.average_rating, reverse=True)
    return result[:]


@pytest.fixture()
def review_result(prepare_db_user_movie_env):
    result = []
    for i, (proxy_class, data) in enumerate(review_proxy_data()):
        user_model, user_data = data.pop('user_data')
        movie_model, movie_data = data.pop('movie_data')
        user = user_model.get(**user_data)
        movie = movie_model.get(**movie_data)
        with create_session() as session:
            proxy_class.create(
                session=session,
                user_id=user.id,
                movie_id=movie.id,
                user=user_model.get_model(session=session, id=user.id),
                movie=movie_model.get_model(session=session, id=movie.id),
                **data,
            )
        result.append(
            proxy_class.get_schema_model(user_id=user.id, movie_id=movie.id)
        )
    result = sorted(result, key=lambda x: x.updated_at, reverse=True)
    for value in result:
        setattr(value, 'updated_at', value.updated_at.isoformat())
    return result[:]


@pytest.fixture()
def test_headers_user_1():
    _, data = user_proxy_data()[0]
    return {'Authorization': f'Basic {data["base64_string"]}'}
