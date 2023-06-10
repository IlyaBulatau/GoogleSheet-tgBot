from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from database.models import User


router = Router()

@router.message(Command(commands=['start']))
async def process_command_start(message: Message):
    User(tg_id=message.from_user.id, username=message.from_user.username).save()
    await message.answer(text='Hello')