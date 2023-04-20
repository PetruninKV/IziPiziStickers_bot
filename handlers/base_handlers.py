from aiogram import Router
from aiogram.filters import CommandStart, Command, Text
from aiogram.types import Message

from lexicon.lexicon import LEXICON_MESSAGE, LEXICON_KEYBOARD
from config_data.config import Config, load_config
from key_boards.start_keyboard import creat_start_keyboard
from services.services import get_point_location

config: Config = load_config()

router: Router = Router()


@router.message(CommandStart())
async def proc_statr_command(message: Message):
    await message.answer(text=LEXICON_MESSAGE['/start'])
    await message.answer_sticker(sticker=config.object_id.welcome_stick)
    await message.answer(text=LEXICON_MESSAGE['/start continue'],
                         reply_markup=creat_start_keyboard(
                             'instruction', 'about you', 'security', 'location'
                         ))

@router.message(Text(text=LEXICON_KEYBOARD['instruction']))
async def proc_mes_instruction(message: Message):
    await message.answer(text=LEXICON_MESSAGE['instruction'])

@router.message(Text(text=LEXICON_KEYBOARD['about you']))
async def proc_mes_about_you(message: Message):
    pass

@router.message(Text(text=LEXICON_KEYBOARD['security']))
async def proc_mes_security(message: Message):
    await message.answer(text=LEXICON_MESSAGE['security'])



@router.message(Text(text=LEXICON_KEYBOARD['location']))
async def proc_mes_location(message: Message):
    await message.answer(text=LEXICON_MESSAGE['location'])
    await message.answer_location(latitude=get_point_location(),
                                  longitude=get_point_location(),
                                  horizontal_accuracy=150,
                                  protect_content=True)

