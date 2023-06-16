from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import TelegramObject, Message, CallbackQuery
from aiogram.utils.chat_action import ChatActionSender
from typing import Awaitable, Callable, Any, Dict

from database.models import User
from config import config
from documents.documents import CALLBACK


class UploadDocumentMiddlware(BaseMiddleware):

    async def __call__(
                self, 
                handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], 
                event: TelegramObject | Message | CallbackQuery, 
                data: Dict[str, Any]):
        

        upload_document_operation = get_flag(handler=data, name='upload_document_operation')

        if upload_document_operation:
            async with ChatActionSender(chat_id=event.chat.id, action=upload_document_operation):
                return await handler(event, data)
            
        return await handler(event, data)
    
class LimitAccessMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: CallbackQuery,
            data: Dict[str, Any]):
        

        user = User.get_user_by_id(event.from_user.id)
        admin_id = config.ADMIN_ID

        flag_vip = get_flag(handler=data, name='flag_vip')

        if flag_vip:
            if not user.vip:    
                return await event.answer(text='Доступно только c VIP', show_alert=False)
        
        return await handler(event, data)
    
class ColorLimitAccessMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: CallbackQuery,
            data: Dict[str, Any]):

        user = User.get_user_by_id(event.from_user.id)
        admin_id = config.ADMIN_ID
        callback = event.data
        colors = [
            CALLBACK['black'],
            CALLBACK['yellow'],
            CALLBACK['brown'],
            CALLBACK['grey'],
        ]
        
        flag_color = get_flag(handler=data, name='flag_color')


        if flag_color:
            if not user.vip:
                if callback in colors:
                    return await event.answer(text='Доступно только c VIP', show_alert=False)
            
        return await handler(event, data)

class FontLimitAccessMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: CallbackQuery,
            data: Dict[str, Any]):

            user = User.get_user_by_id(event.from_user.id)
            admin_id = config.ADMIN_ID
            callback = event.data
            fonts = [
                CALLBACK['georgia'],
                CALLBACK['verdana'],
                CALLBACK['strikethrough']
            ]

            flag_font = get_flag(handler=data, name='flag_font')

            if flag_font:
                if not user.vip:
                    if callback in fonts:
                        return await event.answer(text='Доступно только c VIP', show_alert=False)
            
            return await handler(event, data)

 