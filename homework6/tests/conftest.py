import pathlib

import pytest
from fakeredis import FakeStrictRedis
from fastapi.testclient import TestClient
from PIL import Image
from rq import Queue

from app import utils
from app.__main__ import app
from app.size import Size
from config import cfg

data_path = pathlib.Path(__file__).parent / 'data'


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
def fake_redis(mocker):
    redis = FakeStrictRedis()
    mocker.patch('app.redis_cfg.redis_conn', redis)
    mocker.patch('app.routers.tasks.redis_conn', redis)
    mocker.patch('app.utils.redis_conn', redis)
    return redis


@pytest.fixture()
def fake_queue(mocker, fake_redis):
    queue = Queue(is_async=False, connection=fake_redis)
    mocker.patch('app.redis_cfg.redis_queue', queue)
    mocker.patch('app.routers.tasks.redis_queue', queue)
    return queue


@pytest.fixture()
def images():
    return {
        Size(size): Image.open(data_path / f'normal_{size}.png')
        for size in cfg.allowed_sizes
    }


@pytest.fixture()
def big_images():
    return {
        Size(size): Image.open(data_path / f'big_{size}.png')
        for size in cfg.allowed_sizes
    }


@pytest.fixture()
def image_wrong():
    return Image.open(data_path / 'wrong.png')


@pytest.fixture()
def image_data():
    with open(data_path / 'normal_original_base64.txt', 'r') as f:
        return f.read()


@pytest.fixture()
def big_image_data():
    with open(data_path / 'big_original_base64.txt', 'r') as f:
        return f.read()


@pytest.fixture()
def image_broken_data():
    with open(data_path / 'image_broken_base64.txt', 'r') as f:
        return f.read()


@pytest.fixture()
def images_data(images):
    return {
        Size(size): utils.ImageEncoder.encode(image)
        for size, image in images.items()
    }


@pytest.fixture()
def big_images_data(big_images):
    return {
        Size(size): utils.ImageEncoder.encode(image)
        for size, image in big_images.items()
    }


@pytest.fixture()
def created_task(client, fake_redis, fake_queue, image_data):
    return client.post(
        '/tasks',
        json={
            'data': image_data,
        },
    ).json()


@pytest.fixture()
def created_task_big(client, fake_redis, fake_queue, big_image_data):
    return client.post(
        '/tasks',
        json={
            'data': big_image_data,
        },
    ).json()
