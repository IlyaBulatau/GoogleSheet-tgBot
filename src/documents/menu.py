from aiogram.methods import SetMyCommands
from aiogram.types import BotCommand


def set_menu():
    commands = SetMyCommands(commands=[
        BotCommand(
        command='start',
        description='В начало'
        ),
        BotCommand(
        command='work',
        description='Начать работу'
        ),
        BotCommand(
        command='tables',
        description='Мои таблицы'
        ),
        BotCommand(
        command='vip',
        description='Получить VIP'
        ),
        BotCommand(
        command='cancel',
        description='Завершить процесс',
        )
    ])
    return commands

