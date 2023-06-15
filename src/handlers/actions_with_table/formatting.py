from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Text

from documents.documents import CALLBACK, INSTRUCTION
from handlers.fsm.states import ActionTableForm, ColorFormattingTableForm, FontFormattingTableForm, FormattingTableForm
from services.action_processes import ColorFormattingTable, FontFormattingTable
from keyboards.keyboards import create_kb_for_table_action, create_kb_for_table_formatting, create_kb_for_choice_color, create_kb_for_font_upgrade, create_kb_with_text_styles


router = Router()

@router.callback_query(Text(text=CALLBACK['formatting']))
async def process_formatting_table(callback: CallbackQuery, state: FSMContext):
    """
    Принимает процесс после того как пользователь нажал на кнопку "Форматирование"

    Запускает процесс форматирование предлагает выбрать действия
    """
    data = await state.get_data()
    table_url = data.get('table_url', None)

    await state.set_state(FormattingTableForm.formatting)
    await state.update_data(table_url=table_url)

    await callback.message.answer(text='Вы начали процесс форматирования\nДля возврата к процессу изменения таблицы нажмите "Назад"\nДля завершения процесса /cancel',
                                   reply_markup=create_kb_for_table_formatting())
    
    await callback.answer()    

@router.callback_query(Text(text=CALLBACK['color']), FormattingTableForm.formatting)
async def process_set_color_in_cell(callback: CallbackQuery, state: FSMContext):
    """
    Принимает процесс после того как пользователь нажал кнопку "Изменить цвет"

    Ожидает ввода значения ячейки
    """
    await state.update_data(formatting=callback.data)
    data = await state.get_data()
    table_url = data.get('table_url', None)

    await state.set_state(ColorFormattingTableForm.cell)
    await state.update_data(table_url=table_url)

    await callback.message.answer(text=INSTRUCTION['Color'])
    await callback.answer()

@router.callback_query(Text(text=CALLBACK['font']), FormattingTableForm.formatting)
async def process_set_font_in_table(callback: CallbackQuery, state: FSMContext):
    await state.update_data(formatting=callback.data)
    data = await state.get_data()
    table_url = data.get('table_url', None)

    await state.set_state(FontFormattingTableForm.font)
    await state.update_data(table_url=table_url)

    await callback.message.answer(text='Что хотите поменть?', reply_markup=create_kb_for_font_upgrade())
    await callback.answer()


@router.callback_query(Text(text=CALLBACK['font_style']), FontFormattingTableForm.font)
async def process_get_style_type(callback: CallbackQuery, state: FSMContext):
    await state.update_data(font=callback.data)
    await state.set_state(FontFormattingTableForm.style)

    await callback.message.answer(text='Выберите шрифт', reply_markup=create_kb_with_text_styles())
    await callback.answer()


@router.callback_query(Text(startswith='style_'), FontFormattingTableForm.style)
async def process_get_font_style_choice(callback: CallbackQuery, state: FSMContext):
    await state.update_data(style=callback.data)
    await state.set_state(FontFormattingTableForm.cell)

    await callback.message.answer(text=INSTRUCTION['Font style'])
    await callback.answer()


@router.message(FontFormattingTableForm.cell)
async def process_get_cell_for_font(message: Message, state: FSMContext):
    await state.update_data(cell=message.text)
    
    data = await state.get_data()
    font = data.get('font', None)
    style = data.get('style', None)
    cell = data.get('cell', None)
    table_url = data.get('table_url', None)

    table = FontFormattingTable(table_url)
    table.set_font_style(cell, style)

    await state.set_state(FormattingTableForm.formatting)
    await message.answer(text='Шрифт применен!')
    await message.answer(text='Что делаем дальше?', reply_markup=create_kb_for_table_formatting())

@router.message(ColorFormattingTableForm.cell)
async def process_get_cell_for_color(message: Message, state: FSMContext):
    """
    Принимает значения чейки

    Ожидает выбора цвета
    """
    await state.update_data(cell=message.text)
    await state.set_state(ColorFormattingTableForm.values)

    await message.answer(text='Выберите цвет', reply_markup=create_kb_for_choice_color())


@router.callback_query(Text(text=CALLBACK['rgb']), ColorFormattingTableForm.values)
async def process_get_rgb_color(callback: CallbackQuery, state: FSMContext):
    """
    Принимает процесс после того как пользователь нажал "Указать в фомате RGB"

    Ожидает ввода ячейки
    """
    await state.update_data(values=callback.data)
    await state.set_state(ColorFormattingTableForm.rgb)

    await callback.message.answer(text=INSTRUCTION['RGB'])
    await callback.answer()

@router.message(ColorFormattingTableForm.rgb)
async def process_get_rgb_color(message: Message, state: FSMContext):
    """
    Принимает процесс после ввода rgb

    Выполняет изменения цвета либо выводит информацию о неправильно введенных даннах
    """
    await state.update_data(rgb=message.text)
    data = await state.get_data()

    cell = data.get('cell', None)
    rgb = data.get('rgb', None)
    table_url = data.get('table_url', None)

    table = ColorFormattingTable(table_url)
    sucssesfull = table.set_color_rgb(cell, rgb)
    
    if sucssesfull != 'Suc': # если данные не валидны
        if sucssesfull == 'error rgb': # если не валидно значение rgb
            await state.set_state(ColorFormattingTableForm.rgb)
            await message.answer(text='Вы ввели цвет формата rgb не верно, попробуйте еще раз\n\nДля прекращения работы /cancel щелк')
            return
        elif sucssesfull == 'error cell': # если не валидно значения ячейки
            await state.set_state(ColorFormattingTableForm.cell)
            await message.answer(text='Вы ввели значения ячейки не корректно попробуйте ввести еще раз\n\nДля прекращения работы /cancel щелк')
            return

    await state.set_state(FormattingTableForm.formatting)
    await message.answer(text='Цвет изменен!')
    await message.answer('Продолжим творчество?\n\nДля возврата к изменению таблицы кнопка "Назад"\n\nДля прекращения работы /cancel', reply_markup=create_kb_for_table_formatting())

@router.callback_query(Text(startswith='color_'), ColorFormattingTableForm.values)
async def process_get_color_value(callback: CallbackQuery, state: FSMContext):
    """
    Принимает процесс после выбора цвета пользователем

    Меняет цвет и устанавливает ожидание дальнеших действий по форматированию
    """
    await state.update_data(values=callback.data)
    data = await state.get_data()

    cell = data.get('cell', None)
    values = data.get('values', None)
    table_url = data.get('table_url', None)

    table = ColorFormattingTable(table_url)
    sucssesfull = table.set_color(cell, values)

    if not sucssesfull:
        await state.set_state(ColorFormattingTableForm.cell)
        await callback.message.answer(text='Вы ввели значения ячейки не корректно попробуйте ввести еще раз\n\nДля прекращения работы /cancel щелк')
        await callback.answer()
        return
    
    await state.set_state(FormattingTableForm.formatting)
    await callback.message.answer(text='Цвет изменен!')
    await callback.message.answer(text='Продолжим творчество?\n\nДля возврата к изменению таблицы кнопка "Назад"\n\nДля прекращения работы /cancel', reply_markup=create_kb_for_table_formatting())
    await callback.answer()    



@router.callback_query(Text(text=CALLBACK['back']))
async def process_back(callback: CallbackQuery, state: FSMContext):
    """
    Кнопка назад для выхода из проесса форматирования и переход
    к процессу выбора действий с таблицей
    """
    await state.set_state(ActionTableForm.action)

    await callback.message.answer(text='Продолжим?\nДля выхода из процесса щелкните /cancel', reply_markup=create_kb_for_table_action())
    await callback.answer()
