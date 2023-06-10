import re

from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsPhotoDoc(BaseFilter):
    async def __call__(self, message: Message) -> bool | dict[str, str]:
        allowed_types = ['image/jpeg', 'image/webp', 'image/png']
        if message.document.mime_type in allowed_types:
            return {'file_id': message.document.file_id}
        return False


class IsLinkStickerpack(BaseFilter):
    async def __call__(self, message: Message) -> bool | dict[str, str]:
        pattern = r'^https://t\.me/addstickers/[\w_-]+$'
        url = message.text.split(' ')[1]
        if re.match(pattern, url):
            return {'link': url}
        return False
