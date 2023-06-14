from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, Redis

import asyncio

from config import BaseConfig
from database.connect import create_database, session, engine
from database.models import Base, User, Table

from handlers.commands import router
from handlers.fsm.process import router as fsm_router
from handlers.create_table.handlers import router as create_table_router
from handlers.actions_with_table.action import router as action_router
from handlers.admin.commands import router as admin_router
from handlers.actions_with_table.formatting import router as formatting_router

from documents.menu import set_menu
from config import config
from logger.logger import logger


async def main():
    redis = Redis(host=config.REDIS_HOST)
    storage = RedisStorage(redis)   

    bot = Bot(token=BaseConfig.TOKEN)
    ds = Dispatcher(storage=storage)

    ds.include_routers(router, 
                        fsm_router,
                        create_table_router,
                        action_router,
                        admin_router,
                        formatting_router,
                        )
    
    await bot(set_menu())
    await ds.start_polling(bot)

if __name__ == "__main__":
    create_database()
    Base.metadata.create_all(bind=engine)
    logger.warning('START BOT')
    asyncio.run(main())
    session.remove()
    logger.warning('STOP BOT')