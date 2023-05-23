from aiogram import F, Bot, Router
from aiogram.filters import Command, Text, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from config_data.config import Config, load_config
from lexicon.lexicon import LEXICON_ADMIN
from state.fsm import FSMAdmin
from key_boards.inlinekeyboards import create_inline_kb

config: Config = load_config()

router: Router = Router()
router.message.filter(F.from_user.id == config.tg_bot.admin)


@router.message(Command(commands='admin'))
async def check_admin(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_ADMIN['/admin'])
    await state.set_state(FSMAdmin.admin_work)


@router.message(Command(commands='exit'),
                StateFilter(FSMAdmin.admin_work, FSMAdmin.block, FSMAdmin.send_text))
async def processing_no_admin_command(message: Message, state: FSMContext):
    # выходит из состояний
    await state.clear()
    await message.answer(text='Обычный пользователь')


@router.message(Command(commands='cancel'), StateFilter(FSMAdmin.block, FSMAdmin.input_text))
async def processing_cancel_input(message: Message, state: FSMContext):
    # выходит из состояний
    await state.set_state(FSMAdmin.admin_work)
    await message.answer(text=LEXICON_ADMIN['/admin'])


@router.message(Command(commands='stat'), StateFilter(FSMAdmin.admin_work))
async def processing_stat_command(message: Message):
    await message.answer(text=LEXICON_ADMIN['/stat'])
    # сколько пользователей
    # кто заблокировал бота
    # кто присоеденился


@router.message(Command(commands='block_user'),
                StateFilter(FSMAdmin.admin_work))
async def processing_block_command(message: Message):
    await message.answer(text=LEXICON_ADMIN['/block_user'])


@router.message(Command(commands='unblock_user'),
                StateFilter(FSMAdmin.admin_work))
async def processing_unblock_command(message: Message):
    await message.answer(text=LEXICON_ADMIN['/unblock_user'])


@router.message(Command(commands='black_list'),
                StateFilter(FSMAdmin.admin_work))
async def processing_black_list_command(message: Message):
    await message.answer(text='В списке заблокированных:')


@router.message(Command(commands='text'), StateFilter(FSMAdmin.admin_work))
async def processing_text_command(message: Message, state: FSMContext):
    # входит в режим общения со всеми пользователями
    await message.answer(text=LEXICON_ADMIN['/text'])
    await state.set_state(FSMAdmin.input_text)


@router.message(Text, StateFilter(FSMAdmin.input_text))
async def check_input_message(message: Message, state: FSMContext):
    # отправляет всем пользователям сообщение
    await message.answer(text=f'Проверь сообщение:\n <code>{message.text}</code>',
                         reply_markup=create_inline_kb(2, send='Отправить', cancel='Отменить'))
    await state.update_data(text=message.text)
    await state.set_state(FSMAdmin.send_text)


@router.callback_query(Text(text='send'), StateFilter(FSMAdmin.send_text))
async def send_message_all_users(callback: CallbackQuery, state: FSMContext, bot: Bot):
    admin_message = await state.get_data()
    print(admin_message['text'])
    await bot.send_message(chat_id=000000000, text=admin_message['text'])
    await callback.answer(text='Сообщение отправлено!', show_alert=True)
    await callback.message.edit_text(text=LEXICON_ADMIN['send_text'])
    await state.set_state(FSMAdmin.input_text)


@router.callback_query(Text(text='cancel'), StateFilter(FSMAdmin.send_text))
async def check_your_message(callback: CallbackQuery, state: FSMContext):
    await callback.answer(text='Сообщение удалено!')
    await callback.message.edit_text(text=LEXICON_ADMIN['send_text'])
    await state.set_state(FSMAdmin.input_text)


@router.message(StateFilter(FSMAdmin.send_text))
async def processing_other_messages_in_state_send_text(message: Message):
    pass


@router.message(StateFilter(FSMAdmin.admin_work))
async def processing_other_messages(message: Message):
    await message.answer(text=LEXICON_ADMIN['/admin'])
