from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import TelegramObject, Message, CallbackQuery
from aiogram.utils.chat_action import ChatActionSender
from typing import Awaitable, Callable, Any, Dict

from database.models import User
from config import config


class UploadDocumentMiddlware(BaseMiddleware):

    async def __call__(self, 
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
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject | Message | CallbackQuery,
            data: Dict[str, Any]):
        

        user = User.get_user_by_id(event.from_user.id)
        admin_id = config.ADMIN_ID

        if user.vip or event.from_user.id == int(admin_id):
            return await handler(event, data)
        
        return await event.answer(text='Доступно только c VIP')