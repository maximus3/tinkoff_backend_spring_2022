import fakeredis.aioredis
import pytest
from async_asgi_testclient import TestClient
from httpx import AsyncClient

from app.__main__ import app
from app.redis import redis
from app.user import User


@pytest.fixture()
async def fake_redis(mocker):
    fake_redis = fakeredis.aioredis.FakeRedis()
    mocker.patch.object(redis, '_redis', fake_redis)

    yield fake_redis


@pytest.fixture()
async def client(fake_redis):
    async with AsyncClient(
        app=app, base_url='http://localhost:8090/'
    ) as client:
        yield client


@pytest.fixture()
async def ws_client(fake_redis):
    async with TestClient(app) as client:
        yield client


@pytest.fixture()
async def users(fake_redis):
    users = []
    for i in range(2):
        users.append(await User.register(f'user_{i}'))
    return users
