import asyncio
from typing import Literal

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError

from database.users import active_users, blocked_users

ActionType = Literal['ban', 'unban']


async def send_message_users(message: str, bot: Bot) -> None | str:
    failed_users: set = set()
    for user in active_users:
        await asyncio.sleep(0.1)
        try:
            await bot.send_message(chat_id=user,
                                   text='Сообщение от администратора:\n'
                                   f'<code>{message}</code>')
            print('Сообщение отправилось:', user)
        except TelegramAPIError:
            print('Обработка исключения')
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
