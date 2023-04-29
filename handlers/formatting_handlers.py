import asyncio
import random

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import BufferedInputFile, Message

# FSM
from aiogram.filters import StateFilter
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from lexicon.lexicon import LEXICON_MESSAGE
from config_data.config import Config, load_config
from filters.my_filters import IsPhotoDoc
from services.convert import photo_processing

router: Router = Router()

config: Config = load_config()


class FSMFormatting(StatesGroup):
    work_on = State()


@router.message(Command(commands='formatting'))
async def proc_photo_to_png_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_MESSAGE['/formatting'])
    await state.set_state(FSMFormatting.work_on)
    await message.answer(text=LEXICON_MESSAGE['/formatting_continue'])


@router.message(F.photo[-1].file_id.as_('file_id'), StateFilter(FSMFormatting.work_on))
@router.message(F.document, IsPhotoDoc())
async def convert_photo(message: Message, file_id: str):
    text = random.choice(LEXICON_MESSAGE['reaction_to_photo'])  # noqa: S311
    await message.answer(text=text)
    await asyncio.sleep(1)
    await message.answer(text=LEXICON_MESSAGE['processing'])
    await message.answer_sticker(sticker=config.object_id.processing_stick)
    file_content: bytes | str = await photo_processing(file_id)
    if isinstance(file_content, bytes):
        text_file = BufferedInputFile(file=file_content, filename="file_for_@sticker.png")
        await message.answer_document(document=text_file)
        await message.answer(text=LEXICON_MESSAGE['finish'])
    else:
        await message.answer(text=file_content)


@router.message(Command(commands='stop_formatting'), StateFilter(FSMFormatting.work_on))
async def proc_stop_format_command(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text=LEXICON_MESSAGE['/stop_formatting'])


@router.message(StateFilter(FSMFormatting.work_on))
async def proc_stop_format_command_not_possible(message: Message):
    await message.answer(text=LEXICON_MESSAGE['formatting_work_on'])
