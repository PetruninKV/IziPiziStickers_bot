from redis.asyncio.client import Redis


async def get_users_from_db(redis: Redis, name_key: str):
    users_in_db: set[bytes] = await redis.smembers(name_key)
    users_str = (user for user in users_in_db)
    return '\n'.join(users_str)


async def set_users_db(redis: Redis, name_key: str, users: str):
    users_for_ban = set(users.split('\n'))
    await redis.sadd(name_key, *users_for_ban)


async def rm_users_from_db(redis: Redis, name_key: str, users: str):
    users_for_unban = set(users.split('\n'))
    await redis.srem(name_key, *users_for_unban)
