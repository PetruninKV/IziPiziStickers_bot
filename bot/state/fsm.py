from aiogram.filters.state import State, StatesGroup


class FSMFormatting(StatesGroup):
    work_on = State()


class FSMAdmin(StatesGroup):
    admin_work = State()
    block = State()
    send_text = State()
