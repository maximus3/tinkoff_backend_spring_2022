import aioredis

from app.redis import redis


class Channel:
    def __init__(self, channel_id: str, channel_name: str) -> None:
        self.channel_id = channel_id
        self.channel_name = channel_name

    async def init(self, channel_name: str) -> None:
        tmp_channel = await Channel.register(channel_name)
        self.channel_id = tmp_channel.channel_id
        self.channel_name = tmp_channel.channel_name

    @staticmethod
    async def register(channel_name: str) -> 'Channel':
        channel_id = await redis.register('channels', channel_name)
        return Channel(channel_id, channel_name)

    @staticmethod
    async def get_by_id(channel_id: str) -> 'Channel':
        channel_name = await redis.get_by_id('channels', channel_id)
        return Channel(channel_id, channel_name)

    async def get_history(self, msg_count: int = 50) -> list[str]:
        return await redis.get_history(self.channel_id, msg_count)

    async def add_message(self, username: str, msg: str) -> None:
        await redis.add_message(self.channel_id, f'{username}:{msg}')

    async def subscribe_redis_channel(self) -> aioredis.client.PubSub:
        return await redis.subscribe(self.channel_id)


main_channel = Channel('', '')
