from aiogram import Bot
from aiogram.types import BotCommand

from lexicon.lexicon import LEXICON_MENU


async def set_main_menu(bot: Bot):
    main_menu = [
        BotCommand(command=command, description=description)
        for command, description in LEXICON_MENU.items()
    ]
    await bot.set_my_commands(main_menu)
