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
        InlineKeyboardButton(text='Добавить строку по номеру строки', callback_data=CALLBACK['insert_row_by_index']),
        InlineKeyboardButton(text='Вставить значение в ячейку', callback_data=CALLBACK['set_in_cell']),
        InlineKeyboardButton(text='Изменить название таблицы', callback_data=CALLBACK['rename_table']),
        InlineKeyboardButton(text='Добавить несколько строк в начало', callback_data=CALLBACK['insert_rows']),
        InlineKeyboardButton(text='Добавить несколько строк в в конец', callback_data=CALLBACK['append_rows']),
        InlineKeyboardButton(text='Добавить несколько строк начиная с заданной ячейки', callback_data=CALLBACK['append_rows_cell']),
        InlineKeyboardButton(text='Удалить страку/строки', callback_data=CALLBACK['delete_rows']),
        InlineKeyboardButton(text='Форматирование', callback_data=CALLBACK['formatting']),
    ]

    kb.row(*buttons, width=1)
    

    return kb.as_markup()

def create_kb_for_table_formatting():

    kb = InlineKeyboardBuilder()

    buttons = [
        InlineKeyboardButton(text='Изменить цвет', callback_data=CALLBACK['color']),
        InlineKeyboardButton(text='Изменить шрифт', callback_data=CALLBACK['font']),
        InlineKeyboardButton(text='Назад', callback_data=CALLBACK['back'])
    ]

    kb.row(*buttons, width=1)

    return kb.as_markup()

def create_kb_for_choice_color():
    kb = InlineKeyboardBuilder()

    buttons = [
        InlineKeyboardButton(text='Синий', callback_data=CALLBACK['blue']),
        InlineKeyboardButton(text='Красный', callback_data=CALLBACK['red']),
        InlineKeyboardButton(text='Зелёный', callback_data=CALLBACK['green']),
    ]

    kb.row(*buttons, width=1)

    return kb.as_markup()