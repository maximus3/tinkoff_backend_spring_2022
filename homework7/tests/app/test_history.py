import pytest

from app.channel import main_channel


@pytest.mark.asyncio
async def test_history_get(client, fake_redis):
    resp = await client.get('/history/main')

    assert resp.status_code == 200
    assert resp.json() == {
        'channel_id': main_channel.channel_id,
        'history': [],
    }
