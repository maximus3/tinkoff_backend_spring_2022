import pytest
from flask import get_flashed_messages, url_for

from database import proxy


@pytest.mark.usefixtures('user_logged_in')
def test_index(test_client, user_with_all):
    response = test_client.get('/contests')
    flashed_messages = get_flashed_messages()
    assert len(flashed_messages) == 0
    assert response.status_code == 200


@pytest.mark.usefixtures('user_logged_in')
def test_contest_by_id_404(test_client, user_with_all):
    response = test_client.get('/contests/123123')
    flashed_messages = get_flashed_messages()
    assert len(flashed_messages) == 0
    assert response.status_code == 404


@pytest.mark.usefixtures('user_logged_in')
def test_contest_by_id(test_client, user_with_all):
    response = test_client.get('/contests/1')
    flashed_messages = get_flashed_messages()
    assert len(flashed_messages) == 0
    assert response.status_code == 200


@pytest.mark.usefixtures('user_logged_in')
def test_registration_404(test_client, user_with_all):
    response = test_client.post('/contests/34534534/registration')
    flashed_messages = get_flashed_messages()
    assert len(flashed_messages) == 0
    assert response.status_code == 404


@pytest.mark.usefixtures('user_logged_in')
def test_registration(test_client, user_with_all):
    response = test_client.post('/contests/2/registration')
    flashed_messages = get_flashed_messages()
    assert len(flashed_messages) == 0
    assert response.status_code == 302
    assert response.headers.get('Location') == url_for(
        'contests.contest_by_id', contest_id=2
    )


@pytest.mark.usefixtures('user_logged_in')
def test_registration_registered(test_client, user_with_all):
    response = test_client.post('/contests/1/registration')
    flashed_messages = get_flashed_messages()
    assert len(flashed_messages) == 0
    assert response.status_code == 302
    assert response.headers.get('Location') == url_for(
        'contests.contest_by_id', contest_id=1
    )


@pytest.mark.usefixtures('user_logged_in')
def test_task_by_id_404_contest(test_client, user_with_all):
    response = test_client.get('/contests/5433543/1')
    flashed_messages = get_flashed_messages()
    assert len(flashed_messages) == 0
    assert response.status_code == 404


@pytest.mark.usefixtures('user_logged_in')
def test_task_by_id_404_order(test_client, user_with_all):
    response = test_client.get('/contests/1/435345')
    flashed_messages = get_flashed_messages()
    assert len(flashed_messages) == 0
    assert response.status_code == 404


@pytest.mark.usefixtures('user_logged_in')
def test_task_by_id(test_client, user_with_all):
    response = test_client.get('/contests/1/1')
    flashed_messages = get_flashed_messages()
    assert len(flashed_messages) == 0
    assert response.status_code == 200


@pytest.mark.usefixtures('user_logged_in')
def test_task_by_id_no_reg(test_client, user_with_all):
    response = test_client.get('/contests/2/1')
    flashed_messages = get_flashed_messages()
    assert len(flashed_messages) == 0
    assert response.status_code == 302
    assert response.headers.get('Location') == url_for(
        'contests.contest_by_id', contest_id=2
    )


@pytest.mark.usefixtures('user_logged_in')
def test_submit_404_contest(test_client, user_with_all):
    response = test_client.post('/contests/5433543/1/submit')
    flashed_messages = get_flashed_messages()
    assert len(flashed_messages) == 0
    assert response.status_code == 404


@pytest.mark.usefixtures('user_logged_in')
def test_submit_404_order(test_client, user_with_all):
    response = test_client.post('/contests/1/435345/submit')
    flashed_messages = get_flashed_messages()
    assert len(flashed_messages) == 0
    assert response.status_code == 404


@pytest.mark.usefixtures('user_logged_in')
def test_submit_no_reg(test_client, user_with_all):
    response = test_client.post('/contests/2/1/submit')
    flashed_messages = get_flashed_messages()
    assert len(flashed_messages) == 0
    assert response.status_code == 302
    assert response.headers.get('Location') == url_for(
        'contests.contest_by_id', contest_id=2
    )


@pytest.mark.usefixtures('user_logged_in')
@pytest.mark.usefixtures('fake_queue')
def test_submit(test_client, user_with_all):
    response = test_client.post(
        '/contests/1/1/submit',
        data={
            'code': 'print("Hello, world!")',
        },
    )
    flashed_messages = get_flashed_messages()
    assert len(flashed_messages) == 0
    assert response.status_code == 302
    assert response.headers.get('Location') == url_for(
        'contests.task_by_id', contest_id=1, order=1
    )

    contest = proxy.ContestProxy.get(id=1)
    user_contest = proxy.UserContestProxy.get(user_id=1, contest_id=contest.id)
    c_problem = proxy.ContestProblemProxy.get(contest_id=contest.id, order=1)

    uc_problem = proxy.UserContestProblemProxy.get(
        user_contest_id=user_contest.id, problem_id=c_problem.problem.id
    )
    user_contest = proxy.UserContestProxy.get(
        user_id=user_with_all.id, contest_id=contest.id
    )

    assert uc_problem.status == 'WA'
    assert uc_problem.score == 0
    assert user_contest.score == 0
