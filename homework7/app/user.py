from app.redis import redis


class User:
    def __init__(self, user_id: str, username: str) -> None:
        self.user_id = user_id
        self.username = username

    @staticmethod
    async def register(username: str) -> 'User':
        user_id = await redis.register('users', username)
        return User(user_id, username)

    @staticmethod
    async def get_by_id(user_id: str) -> 'User':
        username = await redis.get_by_id('users', user_id)
        return User(user_id, username)
