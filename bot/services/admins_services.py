import asyncio
from typing import Literal

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError
from redis.asyncio.client import Redis

from database.users import blocked_users
from config_data.config import config
from services.redis import get_users_from_db

ActionType = Literal['ban', 'unban']

redis_users: Redis = Redis(
    host=config.redis.dsn,
    db=config.redis.users_db_id,
    decode_responses=True,
)


async def send_message_users(message: str, bot: Bot) -> None | str:
    failed_users: set[str] = set()
    async with redis_users:
        active_users = await get_users_from_db(
            redis=redis_users,
            name_key='active_users',
            mode_string=False,
        )
    for user in active_users:
        await asyncio.sleep(0.1)
        try:
            await bot.send_message(chat_id=user,
                                   text='Сообщение от администратора:\n'
                                   f'<code>{message}</code>')
            print('Сообщение отправилось:', user)
        except TelegramAPIError:
            failed_users.add(user)
    if failed_users:
        return '\n'.join((map(str, failed_users)))


def change_blacklist(text: str, action: ActionType) -> None:
    new_ids: set = set(id_user for id_user in text.split('\n'))
    actions = {
        'ban': blocked_users.update,
        'unban': blocked_users.difference_update,
    }
    if action in actions:
        actions[action](new_ids)
    else:
        raise ValueError(f"Invalid action: {action}")
