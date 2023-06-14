from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Text

from documents.documents import CALLBACK, INSTRUCTION
from handlers.fsm.states import ActionTableForm, FormattingTableForm
from services.action_processes import ColorFormattingTable
from keyboards.keyboards import create_kb_for_table_action, create_kb_for_table_formatting, create_kb_for_choice_color


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
    await state.set_state(FormattingTableForm.cell)

    await callback.message.answer(text=INSTRUCTION['Color'])
    await callback.answer()

@router.message(FormattingTableForm.cell)
async def process_get_cell_for_color(message: Message, state: FSMContext):
    """
    Принимает значения чейки

    Ожидает выбора цвета
    """
    await state.update_data(cell=message.text)
    await state.set_state(FormattingTableForm.values)

    await message.answer(text='Выберите цвет', reply_markup=create_kb_for_choice_color())

@router.callback_query(Text(startswith='color_'), FormattingTableForm.values)
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

    await state.set_state(FormattingTableForm.formatting)

    table = ColorFormattingTable(table_url)
    sucssesfull = table.set_color(cell, values)

    if not sucssesfull:
        await state.set_state(FormattingTableForm.cell)
        await callback.message.answer(text='Вы ввели значения ячейки не корректно попробуйте ввести еще раз\n\nДля прекращения работы /cancel щелк')
        await callback.answer()
        return

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
