from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from keyboards import keyboards
from handlers.fsm.states import WorkForm, CreateTableForm, ModificationTableForm
from documents.documents import CALLBACK


router = Router()

@router.callback_query(WorkForm.method)
async def procces_chioce_method_working(callback: CallbackQuery, state: FSMContext):
    await state.update_data(method=callback.data)
    await state.clear()
    if callback.data == CALLBACK['create_table']:
        await state.set_state(CreateTableForm.email)
        await callback.message.answer(text='Пожалуйста, отправте мне свой email для того\nчто бы я мог предоставить вам доступ к Google таблицу')

    elif callback.data == CALLBACK['mod_table']:
        await state.set_state(ModificationTableForm.table_url)
        await callback.message.answer(text='Пожалуйста, отправте мне ссылку на Google таблицу')

