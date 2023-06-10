from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message

import asyncio

from config import BaseConfig
from database.connect import create_database, session, engine
from database.models import Base, User
from handlers.handlers import router

async def main():

    bot = Bot(token=BaseConfig.TOKEN)
    ds = Dispatcher()

    ds.include_router(router)

    await ds.start_polling(bot)

if __name__ == "__main__":
    create_database()
    Base.metadata.create_all(bind=engine)
    asyncio.run(main())
    session.remove()