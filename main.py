import asyncio
import logging
import asyncpg

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from handlers import other_handlers, user_handlers
from config_data.config import Config, load_config

from asyncpg.pool import Pool
from middlewares.db_middleware import DataBaseMiddleware
from database.database import create_tables


logger = logging.getLogger(__name__)


async def main():

    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    logger.info('Starting bot')

    config: Config = load_config()

    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    pool_connect: Pool = await asyncpg.create_pool(host=config.con_pool.db.host,
                                                   port=config.con_pool.db.port,
                                                   database=config.con_pool.db.db_name,
                                                   user=config.con_pool.user.user,
                                                   password=config.con_pool.user.password)

    dp.update.middleware.register(DataBaseMiddleware(pool_connect))

    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    await create_tables(user=config.con_pool.user.user,
                        password=config.con_pool.user.password,
                        database=config.con_pool.db.db_name,
                        host=config.con_pool.db.host)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

asyncio.run(main())
