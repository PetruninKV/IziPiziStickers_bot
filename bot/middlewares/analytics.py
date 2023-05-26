from typing import Any, Awaitable, Callable, Dict

from aiogram.dispatcher.flags import get_flag
from aiogram import BaseMiddleware
from aiogram.types import Message
from services.analytics_services import log


class AnalyticsMiddleware(BaseMiddleware):

    MAX_LIMIT_TEXT: int = 50

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        analytics_key = get_flag(data, 'analytics_key')
        match event.content_type.value:
            case 'text':
                action = event.text[:self.MAX_LIMIT_TEXT]
            # case 'photo':
            #     action = 'photo'
            # case 'document':
            #     action = 'document'
            case _:
                action = event.content_type.value
        await log(event.from_user.id, analytics_key, action)
        return await handler(event, data)
