from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Text, Command

from database.models import User

from config import config

router = Router()


@router.message(Command(commands=['statistics']))
async def process_statisics_command(message: Message):
    user_id = message.from_user.id
    if int(user_id) != int(config.ADMIN_ID):
        return
    users = User.get_all_users()
    responce = '\n'.join([f'Username: @{user.username}, ID: {user.tg_id}' for user in users])

    await message.answer(text=responce)
