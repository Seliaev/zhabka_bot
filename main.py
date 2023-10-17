import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from core.database.base import create_table, connect_to_database
from core.database.function_schedules import get_all_time_data
from core.handlers.basic import get_start, get_subscribe_command, get_zhabka, \
    get_help, change_subscribe, get_update_pictures, get_subscribe_time_command, restart_bot
from core.middlewares.base_middleware import Middleware
from core.settings import settings
from core.utils.commands import set_commands
from core.states.st_loop import StateLoop
from core.utils.scheldule_zhabka import send_zhabka_subscriber


async def assert_start(bot: Bot) -> None:
    """
    Отправляет команду на установку команд бота и сообщение об запуске бота администратору.

    :param bot: Инстанс бота.
    :type bot: Bot
    """
    await set_commands(bot)
    await bot.send_message(settings.bots.id_admin, 'Бот запущен')


async def assert_stop(bot: Bot) -> None:
    """
    Отправляет сообщение об остановке бота администратору.

    :param bot: Инстанс бота.
    :type bot: Bot
    """
    await bot.send_message(settings.bots.id_admin, 'Бот остановлен')


async def handle_bot_operations() -> None:
    """
    Обрабатывает операции, связанные с ботом.

    Инициализирует бота, устанавливает обработчики сообщений и запускает бесконечное ожидание новых сообщений.
    """
    logging.basicConfig(level=logging.WARNING,
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                               "(%(filename)s.%(funcName)s(%(lineno)d) - %(message)s")
    bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')
    dp = Dispatcher()

    dp.startup.register(assert_start)
    dp.shutdown.register(assert_stop)

    dp.message.register(restart_bot, Command(commands='restart'))
    dp.message.register(get_start, Command(commands='start'))
    dp.message.register(get_help, Command(commands='help'))
    dp.message.register(get_zhabka, Command(commands='get_zhabka'))
    dp.message.register(change_subscribe, Command(commands='subscribe'))

    dp.message.register(get_subscribe_command, Command(commands='subs'))
    dp.message.register(get_subscribe_time_command, Command(commands='time'))
    dp.message.register(get_update_pictures, Command(commands='updpic'))

    dp.message.middleware(Middleware())

    # Шедулер на отправку сообщений по таймеру.
    scheduler = AsyncIOScheduler()
    result_sub_times = await get_all_time_data()
    if result_sub_times == None:
        chat_id = settings.bots.id_admin
        hour = 0
        minute = 0
    else:
        for user_data_time in result_sub_times:
            chat_id = user_data_time['chat_id']
            scheduled_time = user_data_time['scheduled_time']
            hour = scheduled_time.hour
            minute = scheduled_time.minute
    scheduler.add_job(send_zhabka_subscriber, "cron", hour=hour, minute=minute,
                              args=(bot, chat_id))
    try:
        scheduler.start()
        await dp.start_polling(bot, skip_updates=True)
    finally:
        await bot.session.close()


async def handle_database_operations() -> None:
    """
    Обрабатывает операции, связанные с базой данных.

    Устанавливает соединение с базой данных и создает необходимую таблицу.

    """
    conn = await connect_to_database()
    if conn is not None:
        await create_table()


async def main() -> None:
    """
    Основная функция, объединяющая операции с ботом и базой данных.

    Запускает обработку операций с ботом и базой данных параллельно.

    """

    await asyncio.gather(
        handle_database_operations(),
        handle_bot_operations()
    )


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    StateLoop.st_loop = loop
    loop.run_until_complete(main())
