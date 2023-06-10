from aiogram.types.bot_command import BotCommand
from aiogram.methods import SetMyCommands

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
        description='end process'
        )
    ])
    return commands