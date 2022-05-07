from app.utils import ImageEncoder


def test_tasks_post_empty(
    client, image_wrong, fake_redis, fake_queue, images_data
):
    response = client.post(
        '/tasks',
        json={
            'data': '',
        },
    )
    assert response.status_code == 422


def test_tasks_post_wrong(
    client, image_wrong, fake_redis, fake_queue, images_data
):
    response = client.post(
        '/tasks',
        json={
            'data': ImageEncoder.encode(image_wrong),
        },
    )
    assert response.status_code == 422


def test_tasks_post(client, image_data, fake_redis, fake_queue, images_data):
    response = client.post(
        '/tasks',
        json={
            'data': image_data,
        },
    )
    assert response.status_code == 201
    assert response.json() == {'id': '1', 'status': 'finished'}
    result = fake_redis.hgetall(response.json()['id'])
    for size in result:
        assert result[size].decode() == images_data[size.decode()]


def test_tasks_get_none(client, fake_redis, fake_queue):
    response = client.get(f'/tasks/1')
    assert response.status_code == 404


def test_tasks_get(client, created_task):
    response = client.get(f'/tasks/{created_task["id"]}')
    assert response.status_code == 200


def test_tasks_image_get_none(client, fake_redis, fake_queue):
    response = client.get(f'/tasks/1/image')
    assert response.status_code == 404


def test_tasks_image_get(client, created_task, images_data):
    for size in images_data:
        response = client.get(f'/tasks/{created_task["id"]}/image?size={size}')
        assert response.status_code == 200
        assert response.json() == images_data[size]


def test_tasks_image_get_wrong_size(client, created_task, images_data):
    response = client.get(f'/tasks/{created_task["id"]}/image?size=wrong')
    assert response.status_code == 422


def test_tasks_image_get_big(client, created_task_big, big_images_data):
    for size in big_images_data:
        response = client.get(
            f'/tasks/{created_task_big["id"]}/image?size={size}'
        )
        assert response.status_code == 200
        assert response.json() == big_images_data[size]


def test_tasks_post_broken(client, fake_redis, fake_queue, image_broken_data):
    response = client.post(
        '/tasks',
        json={
            'data': image_broken_data,
        },
    )
    assert response.json() == {
        'detail': [
            {
                'loc': ['body', 'data'],
                'msg': 'Invalid image data',
                'type': 'value_error',
            }
        ]
    }
