from app import app


def test_home_page():
    with app.test_client() as test_client:
        response = test_client.get('/')
        assert response.status_code == 302
        assert response.headers.get('Location') == 'http://localhost/tasks'


def test_tasks_page():
    with app.test_client() as test_client:
        response = test_client.get('/tasks')
        assert response.status_code == 200


def test_add_task_error():
    with app.test_client() as test_client:
        response = test_client.post('/add_task')
        assert response.status_code == 500


def test_complete_error():
    with app.test_client() as test_client:
        response = test_client.post('/complete')
        assert response.status_code == 500


def test_complete_error_no_index():
    with app.test_client() as test_client:
        response = test_client.post(
            '/complete',
            data={
                'complete_btn': 1,
            },
        )
        assert response.status_code == 404


def test_add_task():
    with app.test_client() as test_client:
        response = test_client.post(
            '/add_task',
            data={
                'task_name': 'task 1',
            },
        )
        assert response.status_code == 302
        assert response.headers.get('Location') == 'http://localhost/tasks'


def test_complete():
    with app.test_client() as test_client:
        test_client.post(
            '/add_task',
            data={
                'task_name': 'task 1',
            },
        )
        response = test_client.post(
            '/complete',
            data={
                'complete_btn': 1,
            },
        )
        assert response.status_code == 302
        assert response.headers.get('Location') == 'http://localhost/tasks'
