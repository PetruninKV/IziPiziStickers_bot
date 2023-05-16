from time import sleep

from aiogram import Router, Bot
from aiogram.filters import Command, CommandStart
from aiogram.types import BufferedInputFile, Message

from config_data.config import Config, load_config
from lexicon.lexicon import LEXICON_MESSAGE

flag = {"throttling_key": "default"}

config: Config = load_config()

router: Router = Router()


@router.message(CommandStart(), flags=flag)
async def proc_statr_command(message: Message):
    await message.answer(text=LEXICON_MESSAGE['/start'])
    if config.object_id.welcome_stick:
        await message.answer_sticker(sticker=config.object_id.welcome_stick)
        await message.answer(text=LEXICON_MESSAGE['/start continue'])


@router.message(Command(commands='instruction'), flags=flag)
async def proc_desc_command(message: Message):
    await message.answer(text=LEXICON_MESSAGE['/instruction'])


@router.message(Command(commands='about'), flags=flag)
async def proc_about_command(message: Message):
    await message.answer(text=LEXICON_MESSAGE['/about'])


@router.message(Command(commands='demo'), flags=flag)
async def proc_demo_command(message: Message, bot: Bot):
    await message.answer(text=LEXICON_MESSAGE['/demo'])
    buff_file_in = BufferedInputFile.from_file(
        path='bot/example_photo/photo.jpg', filename='input_file.jpg')
    await message.answer_photo(photo=buff_file_in,
                               caption='До обработки - .jpg 1280x861 px')
    await bot.send_chat_action(chat_id=message.from_user.id,
                               action="upload_document")
    sleep(5)
    buff_file_out = BufferedInputFile.from_file(
        path='bot/example_photo/file_for_@sticker.png',
        filename='file_for_@sticker.png')
    await message.answer_document(document=buff_file_out,
                                  caption='После обработки - .png 512x344 px')
    await message.answer(text=LEXICON_MESSAGE['/demo continue'])


@router.message(Command(commands='stop_formatting'), flags=flag)
async def proc_stop_formatting_command(message: Message):
    await message.answer(text=LEXICON_MESSAGE['/stop_formatting_error'])


@router.message(Command(commands='privacy'), flags=flag)
async def proc_privacy_command(message: Message):
    await message.answer(text=LEXICON_MESSAGE['/privacy'])


@router.message(Command(commands='lang'), flags=flag)
async def proc_lang_command(message: Message):
    await message.answer(text=LEXICON_MESSAGE['/lang'])


@router.message(Command(commands='help'), flags=flag)
async def proc_help_command(message: Message):
    await message.answer(text=LEXICON_MESSAGE['/help'])
