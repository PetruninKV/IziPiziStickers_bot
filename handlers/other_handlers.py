from aiogram import Router, F
from aiogram.filters import Text
from aiogram.types import Message

from lexicon.lexicon import LEXICON_MESSAGE
from filters.my_filters import IsPhotoDoc

router: Router = Router()

@router.message(F.photo)
@router.message(F.document, IsPhotoDoc())
async def proc_photo_or_doc_mes(message: Message):
    await message.answer(text=LEXICON_MESSAGE['photo_doc_mes'])


@router.message(Text)
async def proc_other_mess(message: Message):
    await message.answer(text=LEXICON_MESSAGE['other_mess'])


