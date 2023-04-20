from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from lexicon.lexicon import LEXICON_KEYBOARD


def creat_start_keyboard(*buttons: str) -> ReplyKeyboardMarkup:
    kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
    kb_builder.row(
        *[KeyboardButton(text=LEXICON_KEYBOARD[button] if button in LEXICON_KEYBOARD else button)
        for button in buttons], width=2
    )
    return kb_builder.as_markup(resize_keyboard=True)