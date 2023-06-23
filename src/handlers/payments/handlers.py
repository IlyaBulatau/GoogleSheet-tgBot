from aiogram import Router, Bot
from aiogram.types import CallbackQuery, Message, PreCheckoutQuery
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext

from utils.cache import cache
from documents.documents import VIP, PRICES, EXCHANGE, DAY_PRICE, WEEK_PRICE, MONTH_PRICE, FOREVER_PRICE
from config import config
from logger.logger import logger
from keyboards.keyboards import create_kb_for_check_payment
from services.yoomoney_api.payments import api
from datetime import datetime
from handlers.fsm.states import PaymentForm


router = Router()

############################################################################################################
    #                                                                                               #
    #                    Система оплаты с помощью Aiogram                                           #
    #                                                                                               #
    #                                                                                               #
    #                                                                                               #
############################################################################################################



# @router.callback_query(Text(text=VIP['day']), flags={'flag_get_vip': 'flag_get_vip'})
# async def process_get_vip_in_day(callback: CallbackQuery, bot: Bot):
#     await bot.send_invoice(
#         chat_id=callback.message.chat.id,
#         title='VIP Статус на день',
#         description='В течении всего периода действия VIP статуса вы сможете использовать полный функионал бота, а так же пользоватся им круглосуточно',
#         payload='get_VIP',
#         provider_token=config.PAY_TEST_KEY,
#         currency='rub',
#         prices=[PRICES[0]],
#         is_flexible=False,
#     )

#     await callback.answer()

# @router.callback_query(Text(text=VIP['week']), flags={'flag_get_vip': 'flag_get_vip'})
# async def process_get_vip_in_week(callback: CallbackQuery, bot: Bot):
#     await bot.send_invoice(
#         chat_id=callback.message.chat.id,
#         title='VIP Статус на неделю',
#         description='В течении всего периода действия VIP статуса вы сможете использовать полный функионал бота, а так же пользоватся им круглосуточно',
#         payload='get_VIP',
#         provider_token=config.PAY_TEST_KEY,
#         currency='rub',
#         prices=[PRICES[1]],
#         is_flexible=False,
#     )

#     await callback.answer()

# @router.callback_query(Text(text=VIP['month']), flags={'flag_get_vip': 'flag_get_vip'})
# async def process_get_vip_in_month(callback: CallbackQuery, bot: Bot):
#     await bot.send_invoice(
#         chat_id=callback.message.chat.id,
#         title='VIP Статус на месяц',
#         description='В течении всего периода действия VIP статуса вы сможете использовать полный функионал бота, а так же пользоватся им круглосуточно',
#         payload='get_VIP',
#         provider_token=config.PAY_TEST_KEY,
#         currency='rub',
#         prices=[PRICES[2]],
#         is_flexible=False,
#     )

#     await callback.answer()


# @router.callback_query(Text(text=VIP['forever']), flags={'flag_get_vip': 'flag_get_vip'})
# async def process_get_vip_in_forever(callback: CallbackQuery, bot: Bot):
#     await bot.send_invoice(
#         chat_id=callback.message.chat.id,
#         title='VIP Статус навсегда',
#         description='Вы сможете использовать полный функионал бота, а так же пользоватся им круглосуточно на всегда',
#         payload='get_VIP',
#         provider_token=config.PAY_TEST_KEY,
#         currency='rub',
#         prices=[PRICES[3]],
#         is_flexible=False,
#     )

#     await callback.answer()


# @router.pre_checkout_query(flags={'flag_get_vip': 'flag_get_vip'})
# async def process_pre_checkout_query(pcq: PreCheckoutQuery, bot: Bot):
#     await bot.answer_pre_checkout_query(pcq.id, ok=True)
    

# @router.message(lambda msg: msg.successful_payment, flags={'flag_get_vip': 'flag_get_vip'})
# async def process_successful_payment(message: Message):
#     user_id = message.from_user.id
#     price = int(message.successful_payment.total_amount) // EXCHANGE
    
#     if price == DAY_PRICE:
#         day = 1
#         status = 'day'
#     elif price == WEEK_PRICE:
#         day = 7
#         status = 'week'
#     elif price == MONTH_PRICE:
#         day = 30
#         status = 'month'
#     elif price == FOREVER_PRICE:
#         day = 4000
#         status = 'forever'
    
#     logger.warning(f'USER WITH ID {user_id} PAY VIP STATUS {status} from {price}RUB')
#     await cache.add_vip_in_hash(user_id, status, day)


############################################################################################################
    #                                                                                               #
    #                    Система оплаты с помощью YooMoneyAPI                                       #
    #                                                                                               #
    #                                                                                               #
    #                                                                                               #
############################################################################################################

@router.callback_query(Text(text=VIP['day']), flags={'flag_get_vip': 'flag_get_vip'})
async def process_get_vip_in_day(callback: CallbackQuery, state: FSMContext):
    label = str(callback.from_user.id)+datetime.strftime(datetime.now(), '%Y_%b_%d_%Hh_%Mm_%Ss')
    url = await api.get_payment_url(DAY_PRICE, label=label)

    await state.set_state(PaymentForm.label)
    await state.update_data(days=DAY_PRICE)
    await state.update_data(label=label)

    await callback.message.answer(text=f'Перейдите по ссылку и совершите оплату\nПосле этого нажмите "Проверить оплату"\n\n{url}', reply_markup=create_kb_for_check_payment())
    await callback.answer()


@router.callback_query(Text(text=VIP['week']), flags={'flag_get_vip': 'flag_get_vip'})
async def process_get_vip_in_week(callback: CallbackQuery, state: FSMContext):
    label = str(callback.from_user.id)+datetime.strftime(datetime.now(), '%Y_%b_%d_%Hh_%Mm_%Ss')
    url = await api.get_payment_url(WEEK_PRICE, label=label)

    await state.set_state(PaymentForm.label)
    await state.update_data(days=WEEK_PRICE)
    await state.update_data(label=label)

    await callback.message.answer(text=f'Перейдите по ссылку и совершите оплату\nПосле этого нажмите "Проверить оплату"\n\n{url}', reply_markup=create_kb_for_check_payment())
    
    await callback.answer()

@router.callback_query(Text(text=VIP['month']), flags={'flag_get_vip': 'flag_get_vip'})
async def process_get_vip_in_month(callback: CallbackQuery, state: FSMContext):
    label = str(callback.from_user.id)+datetime.strftime(datetime.now(), '%Y_%b_%d_%Hh_%Mm_%Ss')
    url = await api.get_payment_url(MONTH_PRICE, label=label)

    await state.set_state(PaymentForm.label)
    await state.update_data(days=MONTH_PRICE)
    await state.update_data(label=label)

    await callback.message.answer(text=f'Перейдите по ссылку и совершите оплату\nПосле этого нажмите "Проверить оплату"\n\n{url}', reply_markup=create_kb_for_check_payment())
    
    await callback.answer()


@router.callback_query(Text(text=VIP['forever']), flags={'flag_get_vip': 'flag_get_vip'})
async def process_get_vip_in_forever(callback: CallbackQuery, state: FSMContext):
    label = str(callback.from_user.id)+datetime.strftime(datetime.now(), '%Y_%b_%d_%Hh_%Mm_%Ss')
    url = await api.get_payment_url(FOREVER_PRICE, label=label)

    await state.set_state(PaymentForm.label)
    await state.update_data(days=FOREVER_PRICE)
    await state.update_data(label=label)

    await callback.message.answer(text=f'Перейдите по ссылку и совершите оплату\nПосле этого нажмите "Проверить оплату"\n\n{url}', reply_markup=create_kb_for_check_payment())
    
    await callback.answer()


@router.callback_query(Text(text='check_payment'), PaymentForm.label, flags={'flag_get_vip': 'flag_get_vip'})
async def process_check_payment(callback: CallbackQuery, state: FSMContext):
    """
    Проверяет прошла ли оплата

    Если прошла то добавляет юзера в кэш с таймером на удаления в зависимости на сколько дней юзер купил ВИП статус
    """
    data = await state.get_data()
    label = data.get('label', None)
    days = data.get('days', None)

    if days == DAY_PRICE:
        status = 'day'
    elif days == WEEK_PRICE:
        status = 'week'
    elif days == MONTH_PRICE:
        status = 'month'
    elif days == FOREVER_PRICE:
        status = 'forever'


    payment = await api.check_payments_verification(label)

    if payment:
        await callback.message.answer(text='Оплата прошла!\n\nПриступим к работе /work ?')
        await cache.add_vip_in_hash(callback.from_user.id, status, days)
        logger.critical(f'User with ID {callback.from_user.id} BUY VIP STATUS')
    else:
        await callback.message.answer(text='Не оплачено\n\nДля завершения процесса /cancel')
        logger.critical(f'User with ID {callback.from_user.id} DONT CAN BUY VIP STATUS')
    await callback.answer()