from aiogram.filters.state import State, StatesGroup


class FSMFormatting(StatesGroup):
    work_on = State()


class FSMAdmin(StatesGroup):
    admin_work = State()
    ban = State()
    uban = State()
    input_text = State()
    send_text = State()
