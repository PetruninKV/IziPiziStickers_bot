from aiogram.filters import BaseFilter
from aiogram.types import Message

class IsPhotoDoc(BaseFilter):
    async def __call__(self, message: Message) -> bool | dict[str, str]:
        print('проверка')
        allowed_types = ['image/jpeg', 'image/webp', 'image/png']
        if message.document.mime_type in allowed_types:
            return {'file_id': message.document.file_id}
        print('2')
        return False