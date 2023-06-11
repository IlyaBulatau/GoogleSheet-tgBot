from documents.documents import CALLBACK, INSTRUCTION
from handlers.fsm.states import ActionTableForm
from services.action_processes import ActionTable
from keyboards.keyboards import create_kb_for_table_action

from aiogram import Router
from aiogram.filters import Text
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext


router = Router()

@router.callback_query(Text(text=CALLBACK['insert_row']), ActionTableForm.action)
async def process_insert_row_in_table(callback: CallbackQuery, state: FSMContext):
    await state.update_data(action=callback.data)
    await state.set_state(ActionTableForm.values)

    await callback.message.answer(text=INSTRUCTION['Use row'])

@router.callback_query(Text(text=CALLBACK['append_row']), ActionTableForm.action)
async def process_insert_row_in_table(callback: CallbackQuery, state: FSMContext):
    await state.update_data(action=callback.data)
    await state.set_state(ActionTableForm.values)

    await callback.message.answer(text=INSTRUCTION['Use row'])

@router.message(ActionTableForm.values)
async def process_add_row_in_table(message: Message, state: FSMContext):
    await state.update_data(values=message.text)
    data = await state.get_data()

    action = data['action']
    values = data['values']
    table_url = data['table_url']
    table = ActionTable(table_url, values)

    if action == CALLBACK['insert_row']:
        table.insert_ro_in_table()
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
    
