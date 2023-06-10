from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from documents.documents import CALLBACK


def create_kb_for_choice_methods_work():
    """
    Выбор действия при команде /work
    """

    kb = InlineKeyboardBuilder()

    buttons = [
        InlineKeyboardButton(text='Создать таблицу', callback_data=CALLBACK['create_table']),
        InlineKeyboardButton(text='Модифицировать таблицу', callback_data=CALLBACK['mod_table'])
    ]

    kb.row(*buttons, width=1)

    return kb.as_markup()