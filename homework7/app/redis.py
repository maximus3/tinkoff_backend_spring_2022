import aioredis

from settings import cfg


class RedisWrapper:
    def __init__(self) -> None:
        self._redis = None

    async def init(self) -> None:
        if self._redis is None:
            self._redis = aioredis.Redis.from_url(cfg.REDIS_URL)

    async def register(
        self, obj_name: str, name: str
    ) -> str:  # TODO: if exists
        if self._redis is None:
            raise RuntimeError('Redis not initialized')
        obj_id = await self._redis.incr(obj_name + '_id')
        await self._redis.hset(obj_name, obj_id, name)
        return str(obj_id)

    async def get_by_id(self, obj_name: str, obj_id: str) -> str:
        if self._redis is None:
            raise RuntimeError('Redis not initialized')
        return (await self._redis.hget(obj_name, obj_id)).decode()

    async def get_history(
        self, channel_id: str, msg_count: int, trim: bool = True
    ) -> list[str]:
        if self._redis is None:
            raise RuntimeError('Redis not initialized')
        if trim:
            await self._redis.ltrim(f'history:{channel_id}', -msg_count, -1)
        return await self._redis.lrange(
            f'history:{channel_id}', -msg_count, -1
        )

    async def add_message(self, channel_id: str, msg: str) -> None:
        if self._redis is None:
            raise RuntimeError('Redis not initialized')
        await self._redis.rpush(f'history:{channel_id}', msg)
        await self._redis.publish(f'channel:{channel_id}', msg)

    async def subscribe(self, channel_id: str) -> aioredis.client.PubSub:
        if self._redis is None:
            raise RuntimeError('Redis not initialized')
        psub = self._redis.pubsub()
        await psub.subscribe(f'channel:{channel_id}')
        return psub


redis = RedisWrapper()
