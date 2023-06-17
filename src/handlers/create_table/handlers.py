from aiogram.types import Message, CallbackQuery
from aiogram.filters import Text
from aiogram import Router
from aiogram.fsm.context import FSMContext

from middlewares.middlewares import UploadDocumentMiddlware
from documents.documents import CALLBACK, CONNECT_STATUS
from handlers.fsm.states import CreateTableForm, ModificationTableForm, ActionTableForm
from services.create_table import create
from services.connect_to_table import table_connect
from database.models import User, Table
from config import config
from keyboards.keyboards import create_kb_for_table_action

router = Router()
router.message.middleware(UploadDocumentMiddlware() )

@router.message(CreateTableForm.email)
async def process_get_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await state.set_state(CreateTableForm.name)
    await message.answer(text='Как назовем таблицу?')
    

@router.message(CreateTableForm.name, flags={'upload_document_operation': 'upload_document'})
async def process_get_name(message: Message, state: FSMContext):
    """
    Принимает процесс работы после того как пользователь
    ввел имя таблицы

    Первым делом проверет валидный ли email отправил пользователь
    проверяется в функции create путем обработки искючения которое бросат модуль gspread

    Если email валидный сохраняет email в базе данных для того что бы пользовател не вводить его каждый раз
    в последствии email можно будет удалить либо изменить

    Запускает процесс работы с таблицей fsm который ожидает ввода действия с таблицей
    """
    await state.update_data(name=message.text)
    data = await state.get_data()
    await state.clear()

    email = data['email']
    table_name = data['name']
    
    url = create(email, table_name)
    if url:
        user = User.get_user_by_id(message.from_user.id)
        user.save_email(email=email)
        Table(url=url, user_tg_id=user.tg_id, name=str(table_name)).save()
        await message.answer(text=f'Таблица создана\n🔗 Ссылка: {url}\n\nВаши таблицы можно посмотреть используя команду /tables')

        await state.set_state(ActionTableForm.action)
        await state.update_data(table_url=url)
        await message.answer(text='Процесс работы с таблицей запущен для выхода из процесса щелкните /cancel\n\nЧто будем делать с таблицей?', reply_markup=create_kb_for_table_action())
        return
    
    await message.answer(text='Email который вы отправили не существуют\nПопробуйте заново /work')

@router.message(ModificationTableForm.table_url, flags={'upload_document_operation': 'upload_document'})
async def process_get_table_url(message: Message, state: FSMContext):
    """
    Принимает процесс работы после того как пользователь
    отправил url таблицы которую хочет модифицировать

    Первым делом проверет валидный ли url отправил пользователь
    проверяется в функции table_connect путем обработки искючения которое бросат модуль gspread

    Так же проверяет есть ли доступ боту к этой таблице
    Если нету отправляет инструкцию как дать доступ боту вместе с BOT_EMAIL

    Если url валидный запускает процесс работы с таблицу fsm который ожидает ввода действия с таблицей
    """

    await state.update_data(table_url=message.text)
    data = await state.get_data()

    connect, table_name = table_connect(data['table_url'])

    if connect == CONNECT_STATUS['Invalid']:
        await message.answer(text='Вы передали не корректный URL')
        return
    
    elif connect == CONNECT_STATUS['Api Error']:
        await message.answer(text=f'Похоже у меня нету доступа к изменению этой таблицы\n\
Что бы я мог модифицировать ее, пожалуста предоставте мне доступ\n\
Для этого добавте мой email к пользователям имеющим доступ к таблице\n\
Mой Emai: {config.BOT_EMAIL}\n\nПосле этого начните сначала /work')
        await state.clear()
        return
    
    await state.clear()
    await state.set_state(ActionTableForm.action)
    await state.update_data(table_url=connect)
    Table(url=connect, user_tg_id=message.from_user.id, name=table_name).save()
    await message.answer(text='Процесс работы с таблицей запущен для выхода из процесса щелкните /cancel\n\nЧто будем делать с таблицей?', reply_markup=create_kb_for_table_action())


