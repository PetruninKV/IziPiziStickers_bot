import asyncio
from typing import Literal

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError

from database.users import blocked_users
from services.redis import RedisDB

ActionType = Literal['ban', 'unban']


async def send_message_users(message: str, bot: Bot, redis: RedisDB) -> None | str:
    failed_users: set[str] = set()
    active_users = await redis.get_users_from_db(
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
