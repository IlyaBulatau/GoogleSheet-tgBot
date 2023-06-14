from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Text

from documents.documents import CALLBACK
from handlers.fsm.states import ActionTableForm, FormattingTableForm

from keyboards.keyboards import create_kb_for_table_action, create_kb_for_table_formatting


router = Router()

@router.callback_query(Text(text=CALLBACK['formatting']))
async def process_formatting_table(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    table_url = data.get('table_url', None)

    await state.set_state(FormattingTableForm.formatting)
    await state.update_data(table_url=table_url)

    await callback.message.answer(text='Вы начали процесс форматирования\nДля возврата к изменени таблицы нажмите "Назад"\nДля завершения процесса /cancel',
                                   reply_markup=create_kb_for_table_formatting())
    
    await callback.answer()    

@router.callback_query(Text(text=CALLBACK['back']))
async def process_back(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ActionTableForm.action)

    await callback.message.answer(text='Продолжим?\nДля выхода из процесса щелкните /cancel', reply_markup=create_kb_for_table_action())
    await callback.answer()
