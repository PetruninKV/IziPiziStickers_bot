import random
import asyncio

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, PhotoSize, BufferedInputFile
from services.convert import photo_processing

from lexicon.lexicon import LEXICON_MESSAGE
from config_data.config import load_config, Config
from filters.my_filters import IsPhotoDoc

router: Router = Router()

config: Config = load_config()


@router.message(Command(commands='formatting'))
async def proc_photo_to_png_command(message: Message):
    await message.answer(text='Отлично! Отправь мне фото')


@router.message(F.photo[-1].file_id.as_('file_id'))
@router.message(F.document, IsPhotoDoc())
async def convert_photo(message: Message, file_id: str):
    print(file_id)
    text = random.choice(LEXICON_MESSAGE['reaction_to_photo'])
    await message.answer(text=text)
    await asyncio.sleep(0.5)
    await message.answer(text=LEXICON_MESSAGE['processing'])
    await message.answer_sticker(sticker=config.object_id.processing_stick)
    file_content: bytes = await photo_processing(file_id)
    text_file = BufferedInputFile(file=file_content, filename="file_for_@sticker.png")
    await  message.answer_document(document=text_file)
