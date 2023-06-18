from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from database.models import User, Table
from documents.documents import TEXT, VIP
from handlers.fsm.states import WorkForm
from keyboards import keyboards
from services.yoomoney_api.payments import api


router = Router()

@router.message(Command(commands=['start']))
async def process_command_start(message: Message):
    User(tg_id=message.from_user.id, username=message.from_user.username).save()
    await message.answer(text=TEXT['start'])

@router.message(Command(commands=['cancel']))
async def process_command_cancel(message: Message, state: FSMContext):
    status_state = await state.get_state()
    if status_state == None:
        return
    await state.clear()
    await message.answer(text='Процесс завершен')

@router.message(Command(commands=['work']))
async def procces_command_work(message: Message, state: FSMContext):
    """
    Комадна для старка работы
    Предлагает выбор между - Создание таблицы или Модификации имеющейся
    Запускает fsm для выбора
    """
    await state.set_state(WorkForm.method)
    await message.answer(text='Выберите действие', reply_markup=keyboards.create_kb_for_choice_methods_work())

@router.message(Command(commands=['vip']), flags={'flag_get_vip': 'flag_get_vip'})
async def process_command_vip(message: Message):
    await message.answer(text=VIP['text'], reply_markup=keyboards.create_kb_for_vip())

@router.message(Command(commands=['tables']))
async def process_command_tables(message: Message):
    user = User.get_user_by_id(message.from_user.id)
    response = '\n\n'.join([f'{table.name}: 🔗 {table.url}'for table in user.tablse])

    await message.answer(text=response)

