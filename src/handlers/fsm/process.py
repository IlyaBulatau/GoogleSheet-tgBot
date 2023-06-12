from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, Text

from keyboards import keyboards
from handlers.fsm.states import WorkForm, CreateTableForm, ModificationTableForm
from documents.documents import CALLBACK
from database.models import User


router = Router()

@router.callback_query(WorkForm.method, Text(text=[CALLBACK['create_table']]))
async def procces_start_create_table(callback: CallbackQuery, state: FSMContext):
    """
    Принимает процесс после того как пользователь
    нажал на кнопку "Создать таблицу" 

    Проверяет есть email текущего пользователя
    Если нету то предлагает его отправить
    Если есть то записывает email в fsm и предлагает ввести имя таблицы
    """
    await state.update_data(method=callback.data)
    await state.clear()

    user = User.get_user_by_id(callback.from_user.id)
    if user.email:
        await state.update_data(email=user.email)
        await state.set_state(CreateTableForm.name)
        await callback.message.answer(text='Как назовем таблицу?')
        await callback.answer()
        return
    
    await state.set_state(CreateTableForm.email)
    await callback.message.answer(text='Пожалуйста, отправте мне свой email для того\nчто бы я мог предоставить вам доступ к Google таблице')
    await callback.answer()


@router.callback_query(WorkForm.method, Text(text=[CALLBACK['mod_table']]))
async def process_start_mod_table(callback: CallbackQuery, state: FSMContext):
    """
    Принимает процесс после того как пользователь
    нажал на кнопку "Создать таблицу" 

    Просит у пользователя ссылку на таблицу
    """

    await state.update_data(method=callback.data)
    await state.clear()

    await state.set_state(ModificationTableForm.table_url)
    await callback.message.answer(text='Пожалуйста, отправте мне ссылку на Google таблицу')
    await callback.answer()
