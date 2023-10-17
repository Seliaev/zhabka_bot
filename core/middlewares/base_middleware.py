from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from core.parser.async_wrapper_pic_parser import async_wrapper_parser
from core.settings import settings
from core.utils.reboot_bot import restart_script


class Middleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        """
        Миддлеварь, выполняется после команды.
        Если условие с командой updpic выполняется, вызывает async_wrapper_parser.

        Если условие с командой restart выполняется, вызывает restart_script.

        :param handler: Асинхронный обработчик.
        :type handler: Callable
        :param event: Объект события.
        :type event: TelegramObject
        :param data: Данные.
        :type data: Dict
        """
        await handler(event, data)
        if isinstance(event, Message) and event.text == '/updpic':
            if await async_wrapper_parser():
                await event.bot.send_message(chat_id=event.chat.id, text='Успешно, картинки обновлены')
            else:
                await event.bot.send_message(chat_id=event.chat.id,
                                             text='Картинки не обновлены, возможно проблема с парсером')

        if isinstance(event, Message) and event.text == '/restart':
            if event.chat.id == settings.bots.id_admin:
                restart_script()

