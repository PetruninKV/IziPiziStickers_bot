from typing import Literal

from aiogram import F, Bot, Router
from aiogram.filters import Command, Text, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from config_data.config import config
from lexicon.lexicon import LEXICON_ADMIN
from state.fsm import FSMAdmin
from key_boards.inlinekeyboards import create_inline_kb
from services.admins_services import send_message_users, change_blacklist
from services.redis import RedisDB
from database.users import blocked_users

ActionType = Literal['ban', 'unban']


router: Router = Router()
router.message.filter(F.from_user.id == config.tg_bot.admin)


@router.message(Command(commands='admin'))
async def check_admin(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_ADMIN['/admin'])
    await state.set_state(FSMAdmin.admin_work)


@router.message(Command(commands='exit'),
                StateFilter(FSMAdmin.admin_work, FSMAdmin.input_text))
async def processing_no_admin_command(message: Message, state: FSMContext):
    # выходит из состояния администратора
    await state.clear()
    await message.answer(text='Обычный пользователь')


@router.message(Command(commands='cancel'), StateFilter(FSMAdmin.ban, FSMAdmin.uban, FSMAdmin.input_text))
async def processing_cancel_input(message: Message, state: FSMContext):
    # выходит из особых состояний администратора
    await state.set_state(FSMAdmin.admin_work)
    await message.answer(text=LEXICON_ADMIN['/admin'])


@router.message(Command(commands='stat'), StateFilter(FSMAdmin.admin_work))
async def processing_stat_command(message: Message):
    await message.answer(text=LEXICON_ADMIN['/stat'])
    # сколько пользователей
    # кто заблокировал бота
    # кто присоеденился


@router.message(Command(commands='ban'), StateFilter(FSMAdmin.admin_work))
async def processing_ban_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_ADMIN['/ban'])
    await state.update_data(change_blacklist='ban')
    await state.set_state(FSMAdmin.ban)


@router.message(Command(commands='unban'), StateFilter(FSMAdmin.admin_work))
async def processing_unban_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_ADMIN['/unban'])
    await state.update_data(change_blacklist='unban')
    await state.set_state(FSMAdmin.uban)


@router.message(F.text, StateFilter(FSMAdmin.ban, FSMAdmin.uban))
async def processing_change_blacklist(message: Message, state: FSMContext, redis_session: RedisDB):
    state_dict: dict[str, ActionType] = await state.get_data()
    action = state_dict['change_blacklist']
    change_blacklist(text=message.text, action=action)
    await {  # noqa: W606
        'ban': redis_session.set_users_to_db,
        'unban': redis_session.rm_users_from_db,
    }[action](name_key='blacklist', users=message.text)
    await message.reply(text=LEXICON_ADMIN[action])
    await state.set_state(FSMAdmin.admin_work)


@router.message(Command(commands='blacklist'),
                StateFilter(FSMAdmin.admin_work))
async def processing_black_list_command(message: Message, redis_session: RedisDB):
    block_users = '\n'.join(map(str, blocked_users))
    await message.answer(text=LEXICON_ADMIN['/blacklist'].format(users=block_users))
    user_in_blacklist: str = await redis_session.get_users_from_db(name_key='blacklist')
    await message.answer(text=LEXICON_ADMIN['/blacklist'].format(users=user_in_blacklist))


@router.message(Command(commands='text'), StateFilter(FSMAdmin.admin_work))
async def processing_text_command(message: Message, state: FSMContext):
    # входит в режим общения со всеми пользователями
    await message.answer(text=LEXICON_ADMIN['/text'])
    await state.set_state(FSMAdmin.input_text)


@router.message(Text, StateFilter(FSMAdmin.input_text))
async def check_input_message(message: Message, state: FSMContext):
    await message.answer(text=f'Проверь сообщение:\n <code>{message.text}</code>',
                         reply_markup=create_inline_kb(2, send='Отправить', cancel='Отменить'))
    await state.update_data(text=message.text)
    await state.set_state(FSMAdmin.send_text)


@router.callback_query(Text(text='send'), StateFilter(FSMAdmin.send_text))
async def send_message_all_users(callback: CallbackQuery, state: FSMContext, bot: Bot, redis_session: RedisDB):
    admin_message = await state.get_data()
    delivery_failed_users = await send_message_users(message=admin_message['text'], bot=bot, redis=redis_session)
    await callback.answer(text='Сообщение отправлено!')
    if delivery_failed_users is not None:
        text = LEXICON_ADMIN['send_error'].format(users=delivery_failed_users)
        await callback.message.answer(text=text)
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
