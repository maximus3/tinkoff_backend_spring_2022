import asyncio
from typing import Any

import aioredis.client
import async_timeout
from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketDisconnect

from app.channel import Channel, main_channel
from app.user import User
from app.ws_manager import ws_manager

router = APIRouter(
    prefix='/ws',
    tags=['ws'],
    responses={404: {'description': 'Not found'}},
)


@router.websocket('/{channel_id}/{user_id}')
async def websocket_endpoint(
    websocket: WebSocket, channel_id: str, user_id: str
) -> Any:
    if channel_id == 'main':
        channel = main_channel
    else:
        channel = await Channel.get_by_id(channel_id)
    user = await User.get_by_id(user_id)
    await ws_manager.connect(websocket)

    async def reader(redis_channel: aioredis.client.PubSub) -> None:
        while True:
            try:
                async with async_timeout.timeout(1):
                    message = await redis_channel.get_message()
                    if message is not None and message['type'] == 'message':
                        await ws_manager.broadcast(message['data'].decode())
                    await asyncio.sleep(0.01)
            except asyncio.TimeoutError:
                pass

    psub = await channel.subscribe_redis_channel()
    try:
        asyncio.create_task(reader(psub))
        while True:
            msg = await websocket.receive_text()
            await channel.add_message(user.username, msg)
    except WebSocketDisconnect:
        await ws_manager.disconnect(websocket)
        await ws_manager.broadcast(f'{user.username} disconnected')
        await psub.unsubscribe()
        await psub.close()
