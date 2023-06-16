from documents.documents import CALLBACK, INSTRUCTION
from handlers.fsm.states import ActionTableForm
from services.action_processes import ActionTable
from keyboards.keyboards import create_kb_for_table_action
from database.models import Table
from middlewares.middlewares import LimitAccessMiddleware

from aiogram import Router
from aiogram.filters import Text
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext


router = Router()
router.message.middleware(LimitAccessMiddleware())

@router.callback_query(Text(text=CALLBACK['insert_row']), ActionTableForm.action)
async def process_insert_row_in_table(callback: CallbackQuery, state: FSMContext):
    """
    Принимает процесс после того как пользователь выбрал действия с таблицей нажав кнопку "Добавить строку в начало"

    Устанавливает состояния оживадания ввода значения для таблицы
    """
    await state.update_data(action=callback.data)
    await state.set_state(ActionTableForm.values)

    await callback.message.answer(text=INSTRUCTION['Use row'])
    await callback.answer()

@router.callback_query(Text(text=CALLBACK['append_row']), ActionTableForm.action)
async def process_insert_row_in_table(callback: CallbackQuery, state: FSMContext):
    """
    Принимает процесс после того как пользователь выбрал действия с таблицей нажав кнопку "Добавить строку в конец"

    Устанавливает состояния оживадания ввода значения для таблицы
    """
    await state.update_data(action=callback.data)
    await state.set_state(ActionTableForm.values)

    await callback.message.answer(text=INSTRUCTION['Use row'])
    await callback.answer()

@router.callback_query(Text(text=CALLBACK['insert_row_by_index']), ActionTableForm.action)
async def process_insert_row_by_index_in_table(callback: CallbackQuery, state: FSMContext):
    """
    Принимает процесс после того как пользователь выбрал действия с таблицей нажав кнопку "Добавить строку по номеру строки"

    Устанавливает состояния оживадания ввода значения для таблицы
    """
    await state.update_data(action=callback.data)
    await state.set_state(ActionTableForm.index)

    await callback.message.answer(text='Введите номер строки цифрой')
    await callback.answer()

@router.message(ActionTableForm.index)
async def process_get_index(message: Message, state: FSMContext):
    await state.update_data(index=message.text)
    await state.set_state(ActionTableForm.values)
    data = await state.get_data()
    action = data.get('action', None)
    url = data.get('table_url', None)
    index = data.get('index', None)

    if action == CALLBACK['insert_row_by_index']:
        await message.answer(text=INSTRUCTION['Use row'])
        return
    
    elif action == CALLBACK['delete_rows']:
        table = ActionTable(url)
        
        succsessfull = table.delete_rows(index)
        if not succsessfull:
            await message.answer(text='Вы ввели числа не корректно\nПопробуйте ввести еще раз\n\nДля завершения процесса шелкните /cancel')
            return

        await message.answer(text='Данные очищены')
        await message.answer(text='Продолжим?\nДля выхода из процесса щелкните /cancel', reply_markup=create_kb_for_table_action())
        await state.set_state(ActionTableForm.action)
        return


@router.callback_query(Text(text=CALLBACK['set_in_cell']), ActionTableForm.action)
async def process_set_value_in_cell(callback: CallbackQuery, state: FSMContext):
    """
    Принимает процесс после того как пользователь выбрал действия с таблицей нажав кнопку "Вставить значение в ячейку"

    Устанавливает состояния оживадания ввода ячейки таблицы
    """

    await state.update_data(action=callback.data)
    await state.set_state(ActionTableForm.cell)

    await callback.message.answer(text=INSTRUCTION['Set value in table'][0])
    await callback.answer()

@router.callback_query(Text(text=CALLBACK['rename_table']), ActionTableForm.action)
async def process_rename_table(callback: CallbackQuery, state: FSMContext):
    """
    Принимает процесс после того как пользователь выбрал действия с таблицей нажав кнопку "Изменить название таблицы"

    Устанавливает состояние ожидания ввода имени таблицы
    """
    await state.update_data(action=callback.data)
    await state.set_state(ActionTableForm.table_name)

    await callback.message.answer(text='Введите новый заголовок для таблицы')
    await callback.answer()

@router.callback_query(Text(text=CALLBACK['insert_rows']), ActionTableForm.action)
async def process_insert_more_rows_in_table(callback: CallbackQuery, state: FSMContext):
    """
    Принимает процесс после того как пользователь выбрал действия с таблицей нажав кнопку "Добавить несколько строк в начало"

    Устанавливает состояния оживадания ввода значения для таблицы
    """
    await state.update_data(action=callback.data)
    await state.set_state(ActionTableForm.values)

    await callback.message.answer(text=INSTRUCTION['Use rows'])
    await callback.answer()

@router.callback_query(Text(text=CALLBACK['append_rows']), ActionTableForm.action)
async def process_append_more_rows_in_table(callback: CallbackQuery, state: FSMContext):
    """
    Принимает процесс после того как пользователь выбрал действия с таблицей нажав кнопку "Добавить несколько строк в конец"

    Устанавливает состояния оживадания ввода значения для таблицы
    """
    await state.update_data(action=callback.data)
    await state.set_state(ActionTableForm.values)

    await callback.message.answer(text=INSTRUCTION['Use rows'])
    await callback.answer()

@router.callback_query(Text(text=CALLBACK['append_rows_cell']), ActionTableForm.action)
async def process_append_more_rows_in_cell_table(callback: CallbackQuery, state: FSMContext):
    """
    Принимает процесс после того как пользователь выбрал действия с таблицей нажав кнопку "Добавить несколько строк начиная с заданной ячейки"

    Устанавливает состояния оживадания ввода значения для таблицы
    """
    await state.update_data(action=callback.data)
    await state.set_state(ActionTableForm.cell)

    await callback.message.answer(text=INSTRUCTION['Set value in table'][2])
    await callback.answer()


@router.message(ActionTableForm.cell)
async def process_get_cell(message: Message, state: FSMContext):
    """
    Ожидает ввода ячейки от пользователя

    Устанавливает состояния ожидания ввода значения для ввода в ячейку
    """
    await state.update_data(cell=message.text)
    await state.set_state(ActionTableForm.values)
    data = await state.get_data()
    action = data.get('action', None)

    if action == CALLBACK['set_in_cell']:
        await message.answer(text=INSTRUCTION['Set value in table'][1])
        return

    elif action == CALLBACK['append_rows_cell']:
        await message.answer(text=INSTRUCTION['Use rows'])    


@router.message(ActionTableForm.table_name)
async def process_get_new_table_name(message: Message, state: FSMContext):
    """
    Ожидает ввода имени таблицы

    Создает обьект таблицы и изменяет имя с сохранением в базе данных
    """
    await state.update_data(table_name=message.text)
    
    data = await state.get_data()
    name = data.get('table_name', None)
    table_url = data.get('table_url', None)
    table = ActionTable(table_url)

    table.rename_table(name)
    Table.rename(table_url=table_url, name=name)

    await message.answer(text='Таблица переименована')
    await message.answer(text='Продолжим?\nДля выхода из процесса щелкните /cancel', reply_markup=create_kb_for_table_action())
    await state.set_state(ActionTableForm.action)

@router.callback_query(Text(text=CALLBACK['delete_rows']), ActionTableForm.action)
async def process_delete_rows(callback: CallbackQuery, state: FSMContext):
    await state.update_data(action=callback.data)
    await state.set_state(ActionTableForm.index)

    await callback.message.answer(text=INSTRUCTION['Del rows'])
    await callback.answer()

@router.message(ActionTableForm.values)
async def process_add_row_in_table(message: Message, state: FSMContext):
    """
    Принимает процесс после того как пользователь ввел данные для занесения в таблицу

    Создает обьект действий с таблицей -  ActionTable 

    Извлекает из fsm данные о том какое действие выбрал юзер
    и в зависимсти от выбора выполняет действие с таблицей

    После выполнения действия включает fsm ожидания для выбора дальнейших действий с таблицей   
    """

    await state.update_data(values=message.text)
    data = await state.get_data()

    action = data.get('action', None)
    cell = data.get('cell', None)
    values = data.get('values', None)
    table_url = data.get('table_url', None)
    index = data.get('index', None)
    table = ActionTable(table_url, values)

    if action == CALLBACK['insert_row']:
        table.insert_row_in_table()

        await message.answer(text='Строка добавлена')
        await message.answer(text='Продолжим?\nДля выхода из процесса щелкните /cancel', reply_markup=create_kb_for_table_action())
        await state.set_state(ActionTableForm.action)
        return

    elif action == CALLBACK['append_row']:
        table.append_row_in_table()

        await message.answer(text='Строка добавлена')
        await message.answer(text='Продолжим?\nДля выхода из процесса щелкните /cancel', reply_markup=create_kb_for_table_action())
        await state.set_state(ActionTableForm.action)
        return
    
    elif action == CALLBACK['insert_row_by_index']:
        seccusfull = table.insert_row_by_index(index)
        if not seccusfull:
            await message.answer(text='Вы ввели номер строки не корректно\nПопробуйте еще раз указать номер строки\n\nДля выхода щелкните /cancel')
            await state.set_state(ActionTableForm.index)
            return
        
        await message.answer(text='Строка добавлена')
        await message.answer(text='Продолжим?\nДля выхода из процесса щелкните /cancel', reply_markup=create_kb_for_table_action())
        await state.set_state(ActionTableForm.action)
        return
    
    elif action == CALLBACK['set_in_cell']:
        seccusfull = table.set_value_in_cell(cell, values)

        if not seccusfull:
            await message.answer(text='Вы ввели номер ячейки не корректно, введите еще раз\nДля завершения процесса шелкните /cancel')
            await state.set_state(ActionTableForm.cell)
            return
        await message.answer(text='Готово!')
        await message.answer(text='Продолжим?\nДля выхода из процесса щелкните /cancel', reply_markup=create_kb_for_table_action())
        await state.set_state(ActionTableForm.action)
        return

    elif action == CALLBACK['insert_rows']:
        table.insert_rows_in_table()

        await message.answer(text="Таблица изменена!")
        await message.answer(text='Продолжим?\nДля выхода из процесса щелкните /cancel', reply_markup=create_kb_for_table_action())
        await state.set_state(ActionTableForm.action)
        return

    elif action == CALLBACK['append_rows']:
        table.append_rows_in_table()

        await message.answer(text="Таблица изменена!")
        await message.answer(text='Продолжим?\nДля выхода из процесса щелкните /cancel', reply_markup=create_kb_for_table_action())
        await state.set_state(ActionTableForm.action)
        return

    elif action == CALLBACK['append_rows_cell']:
        table.append_rows_by_cell(cell)

        await message.answer(text="Таблица изменена!")
        await message.answer(text='Продолжим?\nДля выхода из процесса щелкните /cancel', reply_markup=create_kb_for_table_action())
        await state.set_state(ActionTableForm.action)
        return


