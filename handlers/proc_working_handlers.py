from aiogram import Router, F
from aiogram.filters import Command, Text
from aiogram.types import Message, PhotoSize, BufferedInputFile
from services.convert import photo_processing

router: Router = Router()

@router.message(Command(commands='photo_to_png'))
async def proc_photo_to_png_command(message: Message):
    await message.answer(text='Отлично! Отправь мне фото')


@router.message(F.photo[-1].as_('photo'))
async def convert_photo(message: Message, photo: PhotoSize):
    file_content = await photo_processing(photo.file_id, photo.width, photo.height)
    text_file = BufferedInputFile(file=file_content, filename="file_for_@sticker.png")
    await  message.answer_document(document=text_file)

