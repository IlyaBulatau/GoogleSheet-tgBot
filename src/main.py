from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message

import asyncio

from config import BaseConfig

router = Router()

@router.message()
async def echo(message: Message):
    await message.answer('OK')


async def main():

    bot = Bot(token=BaseConfig.TOKEN)
    ds = Dispatcher()

    ds.include_router(router)

    await ds.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())