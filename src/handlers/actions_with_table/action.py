from documents.documents import CALLBACK, INSTRUCTION
from handlers.fsm.states import ActionTableForm

from aiogram import Router
from aiogram.filters import Text
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext


router = Router()

@router.callback_query(ActionTableForm.action, Text(text=CALLBACK['insert_row']))
async def process_insert_row_in_table(callback: CallbackQuery, state: FSMContext):
    await state.update_data(action=callback.data)
    await state.set_state(ActionTableForm.values)

    await callback.message.answer(text=INSTRUCTION['Use row'])

@router.callback_query(ActionTableForm.action, Text(text=CALLBACK['append_row']))
async def process_insert_row_in_table(callback: CallbackQuery, state: FSMContext):
    await state.update_data(action=callback.data)
    await state.set_state(ActionTableForm.values)

    await callback.message.answer(text=INSTRUCTION['Use row'])


