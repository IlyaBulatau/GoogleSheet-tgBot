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

def create_kb_for_table_action():

    kb = InlineKeyboardBuilder()

    buttons = [
        InlineKeyboardButton(text='Добавить строку в начало', callback_data=CALLBACK['insert_row']),
        InlineKeyboardButton(text='Добавить строку в конец', callback_data=CALLBACK['append_row']),
        InlineKeyboardButton(text='Вставить значение в ячейку', callback_data=CALLBACK['set_in_cell']),
        InlineKeyboardButton(text='Изменить название таблицы', callback_data=CALLBACK['rename_table'])
    ]

    kb.row(*buttons, width=1)

    return kb.as_markup()