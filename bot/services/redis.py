from redis.asyncio.client import Redis
from config_data.config import config


class RedisDB(Redis):

    def __init__(self, db: int, host: str = config.redis.dsn, decode_responses: bool = True):
        super().__init__(host=host, db=db, decode_responses=decode_responses)

    async def get_users_from_db(
        self,
        name_key: str,
        mode_string: bool = True,
    ) -> str | set[str]:
        users_in_db: set[str] = await self.smembers(name_key)
        if mode_string:
            return '\n'.join(users_in_db)
        return users_in_db

    async def set_users_to_db(
        self,
        name_key: str,
        users: str,
    ) -> None:
        users_for_ban = set(users.split('\n'))
        await self.sadd(name_key, *users_for_ban)

    async def rm_users_from_db(
        self,
        name_key: str,
        users: str,
    ) -> None:
        users_for_unban = set(users.split('\n'))
        await self.srem(name_key, *users_for_unban)
