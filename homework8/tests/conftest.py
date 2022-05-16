import datetime as dt
import logging
import shutil

import fakeredis
import pytest
from rq import Queue

from app.main import create_app
from config.config import BASE_DIR, cfg
from database import create_session as real_create_session
from database import proxy
from database.proxy import ContestProxy, ProblemProxy
from tests import static_create
from tests.database import tmp_database_engine, tmp_database_name
from tests.database.config import Session, prepare_db, remove_db
from tests.static import user_proxy_data, user_proxy_data_password


@pytest.fixture()
def logger_mock():
    logging.basicConfig()


@pytest.fixture()
def fake_redis(mocker):
    redis = fakeredis.FakeStrictRedis()
    mocker.patch('config.redis.redis_conn', redis)
    return redis


@pytest.fixture()
def fake_queue(mocker, fake_redis):
    queue = Queue(is_async=False, connection=fake_redis)
    mocker.patch('config.redis.redis_queue', queue)
    mocker.patch('app.routers.contests.redis_queue', queue)
    return


@pytest.fixture()
def prepare_db_env(mocker, logger_mock):
    mocker.patch('database.Session', Session)
    mocker.patch('config.config.cfg.DATABASE_NAME', tmp_database_name)
    mocker.patch('config.config.cfg.DATABASE_ENGINE', tmp_database_engine)
    prepare_db()
    yield
    remove_db()


@pytest.fixture()
def prepare_db_user_env(prepare_db_env):
    user_proxy_data_password()[0].create(**user_proxy_data_password()[1])
    yield


@pytest.fixture()
def create_session(prepare_db_env):
    return real_create_session


@pytest.fixture()
def test_client(prepare_db_env):
    with create_app().test_client() as test_client:
        yield test_client


@pytest.fixture()
def user_logged_in(prepare_db_user_env, test_client):
    test_client.post(
        '/login', data={'login': 'username', 'password': 'password'}
    )
    return


@pytest.fixture()
def dirs_mock(mocker, logger_mock):
    base_dir = BASE_DIR / 'tests/dirs'
    for dir_name in ['contests_dir', 'problems_dir', 'checker_dir']:
        mocker.patch.object(cfg, dir_name, base_dir / dir_name)
        (base_dir / dir_name).mkdir(parents=True)

    mocker.patch.object(ContestProxy, 'DIR_PATH', base_dir / 'contests_dir')
    mocker.patch.object(ProblemProxy, 'DIR_PATH', base_dir / 'problems_dir')

    yield
    shutil.rmtree(base_dir)


@pytest.fixture()
def user_with_all(prepare_db_user_env, dirs_mock):
    user = user_proxy_data()[0].get(**user_proxy_data()[1])
    static_create.create_data(user)
    return user


@pytest.fixture()
def code_wa():
    return 'print(1)'


@pytest.fixture()
def code_ok():
    return 'print(sum(list(map(int, input().split()))))'


@pytest.fixture()
def ucp_solution_getter(user_with_all, code_wa, code_ok):
    def get(_type, was_type=''):
        contest = proxy.ContestProxy.get(name='Contest 1')
        user_contest = proxy.UserContestProxy.get(
            user_id=user_with_all.id, contest_id=contest.id
        )
        c_problem = proxy.ContestProblemProxy.get(
            contest_id=contest.id, order=1
        )
        uc_problem = proxy.UserContestProblemProxy.get(
            user_contest_id=user_contest.id, problem_id=c_problem.problem.id
        )
        if _type == 'wa':
            code = code_wa
        elif _type == 'ok':
            code = code_ok
        else:
            raise ValueError('Unknown type')

        if was_type == 'ok':
            uc_problem = uc_problem.update(status='OK', score=100)
            user_contest = user_contest.update(score=100)
        elif was_type == 'ok50':
            uc_problem = uc_problem.update(status='WA', score=50)
            user_contest = user_contest.update(score=50)

        kwargs = {
            'created_at': dt.datetime.now(),
            'user_contest_problem_id': uc_problem.id,
            'code': code,
        }
        proxy.UserContestProblemSolutionProxy.create(**kwargs)
        kwargs.pop('code')

        ucp_solution = proxy.UserContestProblemSolutionProxy.get(**kwargs)

        return (
            ucp_solution,
            kwargs,
            contest,
            user_contest,
            c_problem,
            uc_problem,
        )

    return get


@pytest.fixture()
def job_getter(ucp_solution_getter, mocker):
    def get(ucp_solution):
        mock = mocker.Mock()
        mock.args = (ucp_solution,)
        return mock

    return get
