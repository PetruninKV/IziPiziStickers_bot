import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, User
from redis.asyncio.client import Redis


class BlackListMiddleware(BaseMiddleware):

    def __init__(self, redis: Redis):
        self.redis = redis

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:

        if not isinstance(event, Message):
            logging.debug("%s used not for Message. But %s", self.__class__.__name__, type(event))
            return await handler(event, data)

        event: Message
        user: User = data["event_from_user"]

        logging.info(user)
        user_in_blacklist: bool = await self.redis.sismember('blacklist', str(user.id))
        if user_in_blacklist:
            logging.debug("User %s found in Redis blacklist", user.id)
            return

        return await handler(event, data)
