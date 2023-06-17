from aiogram import Router, Bot
from aiogram.types import CallbackQuery, Message, PreCheckoutQuery
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext

from utils.cache import cache
from documents.documents import VIP, PRICES, EXCHANGE, DAY_PRICE, WEEK_PRICE, MONTH_PRICE, FOREVER_PRICE
from config import config
from logger.logger import logger


router = Router()


@router.callback_query(Text(text=VIP['day']), flags={'flag_get_vip': 'flag_get_vip'})
async def process_get_vip_in_day(callback: CallbackQuery, bot: Bot):
    await bot.send_invoice(
        chat_id=callback.message.chat.id,
        title='VIP Статус на день',
        description='VIP',
        payload='get_VIP',
        provider_token=config.PAY_TEST_KEY,
        currency='rub',
        prices=[PRICES[0]],
        is_flexible=False,
    )

@router.callback_query(Text(text=VIP['week']), flags={'flag_get_vip': 'flag_get_vip'})
async def process_get_vip_in_day(callback: CallbackQuery, bot: Bot):
    await bot.send_invoice(
        chat_id=callback.message.chat.id,
        title='VIP Статус на неделю',
        description='VIP',
        payload='get_VIP',
        provider_token=config.PAY_TEST_KEY,
        currency='rub',
        prices=[PRICES[1]],
        is_flexible=False,
    )


@router.callback_query(Text(text=VIP['month']), flags={'flag_get_vip': 'flag_get_vip'})
async def process_get_vip_in_day(callback: CallbackQuery, bot: Bot):
    await bot.send_invoice(
        chat_id=callback.message.chat.id,
        title='VIP Статус на месяц',
        description='VIP',
        payload='get_VIP',
        provider_token=config.PAY_TEST_KEY,
        currency='rub',
        prices=[PRICES[2]],
        is_flexible=False,
    )


@router.callback_query(Text(text=VIP['forever']), flags={'flag_get_vip': 'flag_get_vip'})
async def process_get_vip_in_day(callback: CallbackQuery, bot: Bot):
    await bot.send_invoice(
        chat_id=callback.message.chat.id,
        title='VIP Статус навсегда',
        description='VIP',
        payload='get_VIP',
        provider_token=config.PAY_TEST_KEY,
        currency='rub',
        prices=[PRICES[3]],
        is_flexible=False,
    )


@router.pre_checkout_query(flags={'flag_get_vip': 'flag_get_vip'})
async def process_pre_checkout_query(pcq: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pcq.id, ok=True)
    

@router.message(lambda msg: msg.successful_payment, flags={'flag_get_vip': 'flag_get_vip'})
async def process_successful_payment(message: Message):
    user_id = message.from_user.id
    price = int(message.successful_payment.total_amount) // EXCHANGE
    
    if price == DAY_PRICE:
        day = 1
        status = 'day'
    elif price == WEEK_PRICE:
        day = 7
        status = 'week'
    elif price == MONTH_PRICE:
        day = 30
        status = 'month'
    elif price == FOREVER_PRICE:
        day = 4000
        status = 'forever'
    
    logger.warning(f'USER WITH ID {user_id} PAY VIP STATUS {status} from {price}RUB')
    await cache.add_vip_in_hash(user_id, status, day)
