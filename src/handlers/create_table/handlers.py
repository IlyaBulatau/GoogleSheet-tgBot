from aiogram.types import Message, CallbackQuery
from aiogram.filters import Text
from aiogram import Router
from aiogram.fsm.context import FSMContext

from documents.documents import CALLBACK, CONNECT_STATUS
from handlers.fsm.states import CreateTableForm, ModificationTableForm, ActionTableForm
from services.create_table import create
from services.connect_to_table import table_connect
from database.models import User
from config import config
from keyboards.keyboards import create_kb_for_table_action

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
    if url:
        user = User.get_user_by_id(message.from_user.id)
        user.save_email(email=email)
        await message.answer(text=f'Таблица создана\nСсылка: {url}')

        await state.set_state(ActionTableForm.action)
        await state.update_data(table_url=url)
        await message.answer(text='Процесс работы с таблицей запущен для выхода из процесса щелкните /cancel/n/nЧто будем делать с таблицей?', reply_markup=create_kb_for_table_action())
        return
    
    await message.answer(text='Email который вы отправили не существуют\nПопробуйте заново /work')

@router.message(ModificationTableForm.table_url)
async def process_get_table_url(message: Message, state: FSMContext):
    await state.update_data(table_url=message.text)
    data = await state.get_data()

    connect = table_connect(data['table_url'])

    if connect == CONNECT_STATUS['Invalid']:
        await message.answer(text='Вы передали не корректный URL')
        return
    
    elif connect == CONNECT_STATUS['Api Error']:
        await message.answer(text=f'Похоже у меня нету доступа к изменению этой таблицы\n\
Что бы я мог модифицировать ее, пожалуста предоставте мне доступ\n\
Для этого добавте мой email к пользователям имеющим доступ к таблице\n\
Mой Emai: {config.BOT_EMAIL}')
        await state.clear()
        return
    
    await state.clear()
    await state.set_state(ActionTableForm.action)
    await state.update_data(table_url=connect)
    await message.answer(text='Процесс работы с таблицей запущен для выхода из процесса щелкните /cancel/n/nЧто будем делать с таблицей?', reply_markup=create_kb_for_table_action())


