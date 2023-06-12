from aiogram.methods import SetMyCommands
from aiogram.types import BotCommand


def set_menu():
    commands = SetMyCommands(commands=[
        BotCommand(
        command='start',
        description='greeting'
        ),
        BotCommand(
        command='work',
        description='start working'
        ),
        BotCommand(
        command='cancel',
        description='end process',
        )
    ])
    return commands

