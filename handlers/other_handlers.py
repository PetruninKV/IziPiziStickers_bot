from aiogram import Router
from aiogram.filters import Text
from aiogram.types import Message

from lexicon.lexicon import LEXICON_MESSAGE

router: Router = Router()

@router.message(Text)
async def proc_other_mess(message: Message):
    await message.answer(text=LEXICON_MESSAGE['other_mess'])