from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
import asyncio

from config import BaseConfig
from database.connect import create_database, session, engine
from database.models import Base, User, Table
from middlewares.middlewares import WorkTimeLimitAccessMiddleware

from handlers.commands import router
from handlers.fsm.process import router as fsm_router
from handlers.create_table.handlers import router as create_table_router
from handlers.actions_with_table.action import router as action_router
from handlers.admin.commands import router as admin_router
from handlers.actions_with_table.formatting import router as formatting_router
from handlers.payments.handlers import router as payments_router

from utils.cache import redis
from documents.menu import set_menu
from logger.logger import logger


async def main():
    storage = RedisStorage(redis)   

    bot = Bot(token=BaseConfig.TOKEN)
    ds = Dispatcher(storage=storage)
    
    ds.message.middleware(WorkTimeLimitAccessMiddleware())
    ds.callback_query.middleware(WorkTimeLimitAccessMiddleware())

    ds.include_routers(router, 
                        fsm_router,
                        create_table_router,
                        action_router,
                        admin_router,
                        formatting_router,
                        payments_router,
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

# TODO - сделать мультизычность
# TODO - переписать обращения к базе данных на асинхронные вызовы