from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import TelegramObject, Message, CallbackQuery
from aiogram.utils.chat_action import ChatActionSender
from typing import Awaitable, Callable, Any, Dict

from database.models import User
from config import config
from documents.documents import CALLBACK
from utils.cache import cache

from datetime import datetime


class UploadDocumentMiddlware(BaseMiddleware):
    """
    Для продолжительнных хендлеров
    Пишет в левом углу в странице чата >>> загрузка файла
    """

    async def __call__(
                self, 
                handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], 
                event: TelegramObject | Message | CallbackQuery, 
                data: Dict[str, Any]):
        

        upload_document_operation = get_flag(handler=data, name='upload_document_operation')

        # если в хеднлере указан флаг то запускает процесс отображения операции
        if upload_document_operation:
            async with ChatActionSender(chat_id=event.chat.id, action=upload_document_operation):
                return await handler(event, data)
            
        return await handler(event, data)
    
class LimitAccessMiddleware(BaseMiddleware):
    """
    Ограничивает доступ к функионалу бота
    """

    async def __call__(
            self,
            handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: CallbackQuery,
            data: Dict[str, Any]):
        

        user_id = event.from_user.id
        admin_id = config.ADMIN_ID

        flag_vip = get_flag(handler=data, name='flag_vip')

        if flag_vip:
            if not await cache.get_vip_in_hash(user_id):    
                return await event.answer(text='Доступно только c VIP', show_alert=False)
        
        return await handler(event, data)
    
class ColorLimitAccessMiddleware(BaseMiddleware):
    """
    Ограничивает доступ к функионалу бота
    """
    async def __call__(
            self,
            handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: CallbackQuery,
            data: Dict[str, Any]):

        user_id = event.from_user.id
        admin_id = config.ADMIN_ID
        callback = event.data
        colors = [
            CALLBACK['black'],
            CALLBACK['yellow'],
            CALLBACK['brown'],
            CALLBACK['grey'],
        ]
        
        flag_color = get_flag(handler=data, name='flag_color')

        # если пользователь нажал на кнопку цвета и у него нету ВИПа то е пропускать его
        if flag_color:
            if not await cache.get_vip_in_hash(user_id):
                if callback in colors:
                    return await event.answer(text='Доступно только c VIP', show_alert=False)
            
        return await handler(event, data)

class FontLimitAccessMiddleware(BaseMiddleware):
    """
    Ограничивает доступ к функионалу бота
    """
    async def __call__(
            self,
            handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: CallbackQuery,
            data: Dict[str, Any]):

        user_id = event.from_user.id
        admin_id = config.ADMIN_ID
        callback = event.data
        fonts = [
            CALLBACK['georgia'],
            CALLBACK['verdana'],
            CALLBACK['strikethrough']
        ]

        flag_font = get_flag(handler=data, name='flag_font')

        if flag_font:
            if not await cache.get_vip_in_hash(user_id):
                if callback in fonts:
                    return await event.answer(text='Доступно только c VIP', show_alert=False)
        
        return await handler(event, data)

 
class WorkTimeLimitAccessMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]):

        user_id = event.from_user.id
        admin_id = config.ADMIN_ID

        flag_get_vip = get_flag(handler=data, name='flag_get_vip')
        
        if flag_get_vip: # если пользователь запускает процесс приобретния випки
            return await handler(event, data)

        if not await cache.get_vip_in_hash(user_id):
            if int(datetime.today().weekday()) not in (0, 1, 2, 3, 4):
                    if isinstance(event, Message):
                        return event.answer(text='Бот не работает по выходным\n\nДля использования бота круглосуточно\nприобретите VIP статус /vip')
                    elif isinstance(event, CallbackQuery):
                        return event.message.answer(text='Бот не работает по выходным\n\nДля использования бота круглосуточно\nприобретите VIP статус /vip')
        return await handler(event, data)
    
