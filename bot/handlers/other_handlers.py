from aiogram import Router, F
from aiogram.filters import Text
from aiogram.types import Message

from lexicon.lexicon import LEXICON_MESSAGE
from filters.my_filters import IsPhotoDoc

flag = {'throttling_key': 'flood', 'analytics_key': 'flood'}

router: Router = Router()


@router.message(F.photo, flags=flag)
@router.message(F.document, IsPhotoDoc(), flags=flag)
async def proc_photo_or_doc_mes(message: Message):
    await message.answer(text=LEXICON_MESSAGE['photo_doc_mes'])


@router.message(Text, flags=flag)
async def proc_other_mess(message: Message):
    await message.answer(text=LEXICON_MESSAGE['other_mess'])
