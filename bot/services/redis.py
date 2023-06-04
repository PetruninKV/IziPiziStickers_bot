from redis.asyncio.client import Redis


async def get_users_from_db(redis: Redis, name_key: str, mode_string: bool = True) -> str:
    users_in_db: set[str] = await redis.smembers(name_key)
    # users_str = (user for user in users_in_db)
    if mode_string:
        return '\n'.join(users_in_db)
    return users_in_db


async def set_users_db(redis: Redis, name_key: str, users: str):
    users_for_ban = set(users.split('\n'))
    await redis.sadd(name_key, *users_for_ban)


async def rm_users_from_db(redis: Redis, name_key: str, users: str):
    users_for_unban = set(users.split('\n'))
    await redis.srem(name_key, *users_for_unban)
