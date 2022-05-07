import pytest


@pytest.mark.asyncio
async def test_login_post(client, fake_redis):
    resp = await client.post('/login', json={'username': 'username'})

    assert resp.status_code == 201
    assert resp.json()['username'] == 'username'
    assert (
        await fake_redis.hget('users', resp.json()['id'])
    ).decode() == 'username'
