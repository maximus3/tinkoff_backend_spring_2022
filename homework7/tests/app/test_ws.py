import async_timeout
import pytest


@pytest.mark.asyncio
async def test_websocket_one(ws_client, fake_redis, users):
    async with ws_client.websocket_connect(
        f'/ws/main/{users[0].user_id}'
    ) as ws:
        await ws.send_text('HELLO')
        async with async_timeout.timeout(5):
            received_message = await ws.receive_text()
            assert received_message == f'{users[0].username}:HELLO'


@pytest.mark.asyncio
async def test_websocket_two(ws_client, fake_redis, users):
    async with ws_client.websocket_connect(
        f'/ws/main/{users[0].user_id}'
    ) as ws_1:
        async with ws_client.websocket_connect(
            f'/ws/main/{users[1].user_id}'
        ) as ws_2:
            await ws_1.send_text('HELLO')

            async with async_timeout.timeout(5):
                await ws_1.receive_text()
                assert (
                    await ws_1.receive_text() == f'{users[0].username}:HELLO'
                )

            async with async_timeout.timeout(5):
                await ws_2.receive_text()
                assert (
                    await ws_2.receive_text() == f'{users[0].username}:HELLO'
                )

            await ws_2.send_text('HELLO2')

            async with async_timeout.timeout(5):
                assert (
                    await ws_1.receive_text() == f'{users[1].username}:HELLO2'
                )

            async with async_timeout.timeout(5):
                assert (
                    await ws_2.receive_text() == f'{users[1].username}:HELLO2'
                )

        async with async_timeout.timeout(5):
            await ws_1.receive_text()
            assert (
                await ws_1.receive_text()
                == f'{users[1].username} disconnected'
            )
