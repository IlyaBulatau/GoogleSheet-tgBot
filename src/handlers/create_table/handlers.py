from aiogram.types import Message, CallbackQuery
from aiogram.filters import Text
from aiogram import Router
from aiogram.fsm.context import FSMContext

from documents.documents import CALLBACK
from handlers.fsm.states import CreateTableForm
from services.create_table import create


router = Router()


@router.message(CreateTableForm.email)
async def process_get_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await state.set_state(CreateTableForm.name)
    await message.answer(text='Как назовем таблицу?')

@router.message(CreateTableForm.name)
async def process_get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()
    await state.clear()

    email = data['email']
    table_name = data['name']
    
    url = create(email, table_name)
    await message.answer(text=f'Таблица создана\nСсылка {url}')
