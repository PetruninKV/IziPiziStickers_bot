from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from lexicon.lexicon import LEXICON_MESSAGE
from config_data.config import Config, load_config

config: Config = load_config()

router: Router = Router()


@router.message(CommandStart())
async def proc_statr_command(message: Message):
    await message.answer(text=LEXICON_MESSAGE['/start'])
    await message.answer_sticker(sticker=config.object_id.welcome_stick)
    await message.answer(text=LEXICON_MESSAGE['/start continue'])


@router.message(Command(commands='instruction'))
async def proc_desc_command(message: Message):
    await message.answer(text=LEXICON_MESSAGE['/instruction'])


@router.message(Command(commands='about'))
async def proc_about_command(message: Message):
    await message.answer(text=LEXICON_MESSAGE['/about'])


@router.message(Command(commands='demo'))
async def proc_demo_command(message: Message):
    await message.answer(text=LEXICON_MESSAGE['/demo'])


@router.message(Command(commands='privacy'))
async def proc_privacy_command(message: Message):
    await message.answer(text=LEXICON_MESSAGE['/privacy'])


@router.message(Command(commands='lang'))
async def proc_lang_command(message: Message):
    await message.answer(text=LEXICON_MESSAGE['/lang'])


@router.message(Command(commands='help'))
async def proc_help_command(message: Message):
    await message.answer(text=LEXICON_MESSAGE['/help'])
