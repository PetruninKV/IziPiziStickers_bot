import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage, Redis

from config_data.config import Config, load_config
from handlers import adminmode, base_handlers, formatting_handlers, other_handlers, service_handlers
from key_boards.main_menu import set_main_menu
from middlewares.throttling import ThrottlingMiddleware
from middlewares.blacklist import BlackListMiddleware
from middlewares.analytics import AnalyticsMiddleware

logger = logging.getLogger(__name__)


async def main():

    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info('Starting bot')

    config: Config = load_config()

    if config.fsm_mode.mode == 'memory':
        storage: MemoryStorage = MemoryStorage()
    else:
        redis_fsm: Redis = Redis(host=config.redis.dsn, db=config.redis.fsm_db_id)
        storage: RedisStorage = RedisStorage(redis=redis_fsm)

    bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp: Dispatcher = Dispatcher(storage=storage)
    dp.message.filter(F.chat.type == 'private')

    await set_main_menu(bot)

    dp.include_router(service_handlers.router)
    dp.include_router(adminmode.router)
    dp.include_router(formatting_handlers.router)
    dp.include_router(base_handlers.router)
    dp.include_router(other_handlers.router)

    redis_users: Redis = Redis(host=config.redis.dsn, db=config.redis.users_db_id)

    dp.message.outer_middleware(BlackListMiddleware(redis=redis_users))
    dp.message.middleware(ThrottlingMiddleware())
    dp.message.middleware(AnalyticsMiddleware())

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error('Bot stopped!')
