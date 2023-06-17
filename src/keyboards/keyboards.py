from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from documents.documents import CALLBACK, VIP


def create_kb_for_choice_methods_work():
    """
    Выбор действия при команде /work
    """

    kb = InlineKeyboardBuilder()

    buttons = [
        InlineKeyboardButton(text='📗 Создать таблицу', callback_data=CALLBACK['create_table']),
        InlineKeyboardButton(text='📘 Модифицировать таблицу', callback_data=CALLBACK['mod_table'])
    ]

    kb.row(*buttons, width=1)

    return kb.as_markup()

def create_kb_for_table_action():

    kb = InlineKeyboardBuilder()

    buttons = [
        InlineKeyboardButton(text='⬆️ Добавить строку в начало', callback_data=CALLBACK['insert_row']),
        InlineKeyboardButton(text='⬇️ Добавить строку в конец', callback_data=CALLBACK['append_row']),
        InlineKeyboardButton(text='#️⃣ Добавить строку по номеру строки', callback_data=CALLBACK['insert_row_by_index']),
        InlineKeyboardButton(text='📋 Вставить значение в ячейку', callback_data=CALLBACK['set_in_cell']),
        InlineKeyboardButton(text='📋 Изменить название таблицы', callback_data=CALLBACK['rename_table']),
        InlineKeyboardButton(text='⬆️ Добавить несколько строк в начало', callback_data=CALLBACK['insert_rows']),
        InlineKeyboardButton(text='⬇️ Добавить несколько строк в в конец', callback_data=CALLBACK['append_rows']),
        InlineKeyboardButton(text='#️⃣ Добавить несколько строк начиная с заданной ячейки', callback_data=CALLBACK['append_rows_cell']),
        InlineKeyboardButton(text='➖ Удалить страку/строки', callback_data=CALLBACK['delete_rows']),
        InlineKeyboardButton(text='📚 Форматирование', callback_data=CALLBACK['formatting']),
    ]

    kb.row(*buttons, width=1)
    

    return kb.as_markup()

def create_kb_for_table_formatting():

    kb = InlineKeyboardBuilder()

    buttons = [
        InlineKeyboardButton(text='🍅 Изменить цвет ячейки', callback_data=CALLBACK['color']),
        InlineKeyboardButton(text='📜 Изменить текст', callback_data=CALLBACK['font']),
        InlineKeyboardButton(text='Назад', callback_data=CALLBACK['back'])
    ]

    kb.row(*buttons, width=1)

    return kb.as_markup()

def create_kb_for_choice_color():
    kb = InlineKeyboardBuilder()

    buttons = [
        InlineKeyboardButton(text='🔵 Синий', callback_data=CALLBACK['blue']),
        InlineKeyboardButton(text='🔴 Красный', callback_data=CALLBACK['red']),
        InlineKeyboardButton(text='🟢 Зелёный', callback_data=CALLBACK['green']),
        InlineKeyboardButton(text='⚪ Белый', callback_data=CALLBACK['white']),
        InlineKeyboardButton(text='⚫ Чёрный', callback_data=CALLBACK['black']),
        InlineKeyboardButton(text='🟡 Жёлтый', callback_data=CALLBACK['yellow']),
        InlineKeyboardButton(text='🔘 Серый', callback_data=CALLBACK['grey']),
        InlineKeyboardButton(text='🟤 Коричневый', callback_data=CALLBACK['brown']),
        InlineKeyboardButton(text='🎨 Указать в формате RGB', callback_data=CALLBACK['rgb']),
    ]

    kb.row(*buttons, width=2)

    return kb.as_markup()

def create_kb_for_font_upgrade():

    kb = InlineKeyboardBuilder()

    buttons = [
        InlineKeyboardButton(text='☑ Изменить стиль шрифта', callback_data=CALLBACK['font_style']),
        InlineKeyboardButton(text='☑ Изменить цвет текста', callback_data=CALLBACK['font_color']),
        InlineKeyboardButton(text='☑ Изменить размер текста', callback_data=CALLBACK['font_size']),
    ]

    kb.row(*buttons, width=1)

    return kb.as_markup()

def create_kb_with_text_styles():

    kb = InlineKeyboardBuilder()

    buttons = [
        InlineKeyboardButton(text='Жирный', callback_data=CALLBACK['bold']),
        InlineKeyboardButton(text='Georgia', callback_data=CALLBACK['georgia']),
        InlineKeyboardButton(text='Italic', callback_data=CALLBACK['italic']),
        InlineKeyboardButton(text='Verdana', callback_data=CALLBACK['verdana']),
        InlineKeyboardButton(text='Зачеркнутый', callback_data=CALLBACK['strikethrough']),
        InlineKeyboardButton(text='Подчеркнутый', callback_data=CALLBACK['underline']),
    ]

    kb.row(*buttons, width=2)

    return kb.as_markup()

def create_kb_for_vip():

    kb = InlineKeyboardBuilder()

    buttons = [
        InlineKeyboardButton(text='✨ На день', callback_data=VIP['day']),
        InlineKeyboardButton(text='⭐ На неделю', callback_data=VIP['week']),
        InlineKeyboardButton(text='👑 На месяц', callback_data=VIP['month']),
        InlineKeyboardButton(text='💎 Навсегда', callback_data=VIP['forever']),
    ]

    kb.row(*buttons, width=1)

    return kb.as_markup()