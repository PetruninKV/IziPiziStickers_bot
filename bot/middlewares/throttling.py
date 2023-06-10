from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import Message
from cachetools import TTLCache

from lexicon.lexicon import LEXICON_MIDDLEWARES


class ThrottlingMiddleware(BaseMiddleware):
    caches = {
        'formatting': TTLCache(maxsize=10_000, ttl=10),
        'default': TTLCache(maxsize=10_000, ttl=1),
        'flood': TTLCache(maxsize=10_000, ttl=20),
        'flood_feedback': TTLCache(maxsize=10_000, ttl=15),
    }

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        throttling_key = get_flag(data, 'throttling_key')
        if throttling_key is not None and throttling_key in self.caches:
            if event.chat.id in self.caches[throttling_key]:
                if self.caches[throttling_key][event.chat.id]:
                    self.caches[throttling_key][event.chat.id] = False
                    return await event.reply(text=LEXICON_MIDDLEWARES[throttling_key])
                else:
                    return
            else:
                self.caches[throttling_key][event.chat.id] = True
        return await handler(event, data)
