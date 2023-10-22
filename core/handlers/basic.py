from datetime import datetime
from aiogram.types import Message, FSInputFile
from core.parser.async_wrapper_pic_parser import async_wrapper_parser
from core.settings import settings
from core.database.function_schedules import insert_schedule, delete_schedule, \
    get_all_time_data
from core.database.function_users import insert_data_in_table, get_data_from_user_id, get_all_subscribed_users, \
    update_subscribe_status
from core.utils.check_day_wednesday import today_is_wednesday
from core.utils.photo_zhabka import get_random_image, delete_file
from core.utils.reboot_bot import restart_script


# Команды пользователя
async def get_start(message: Message) -> None:
    """
    Обработчик команды /start.
    Проверяет наличие пользователя в БД, если нет - добавляет.

    :param message: Сообщение от пользователя.
    :type message: Message
    """
    id_user = message.from_user.id
    first_name = message.from_user.first_name
    if await insert_data_in_table(user_id=id_user, username=first_name, subscribe=False):
        await message.answer(f'Привет, {first_name}!\nДавай знакомиться?\n'
                             f'Что бы узнать обо мне больше введи /help')
    else:
        await message.answer(f'Привет, {first_name}!\nДавно не виделись!\n'
                             f'Введи команду /help, что бы узнать что тут и как.')


async def get_help(message: Message) -> None:
    """
    Обработчик команды /help.

    :param message: Сообщение от пользователя.
    :type message: Message
    """
    help_text = """
    👋 Добро пожаловать в бота с жабками!

    Что вы можете сделать с этим ботом:
    1. Подписаться на рассылку картинок с жабами:
       - Введите <code>/subscribe 1</code> для подписки.
       - Рассылка происходит каждую среду.

    2. Отписаться от рассылки:
       - Введите <code>/subscribe 0</code> для отписки.

    3. Получить смешную картинку с жабой:
       - Введите /get_zhabka и наслаждайтесь (но сперва подписка)!

    Не забудьте подписаться на рассылку, чтобы не пропустить новых жабок 🐸
    """
    await message.answer(help_text)



async def get_zhabka(message: Message) -> None:
    """
    Отправляет пользователю случайное изображение жабы (кроме среды) по команде /get_zhabka, если он подписан.

    :param message: Объект сообщения пользователя.
    :type message: Message
    """
    id_user = message.from_user.id
    result_data = await get_data_from_user_id(id_user)
    if result_data['subscribe']:
        path_to_zhabka = get_random_image('wednesday')
        if path_to_zhabka == "":
            await message.answer(f'Жабки кончились, подожди пару минут, я их поймаю.\nЧерез пару минут снова отправь команду.')
            await async_wrapper_parser() # Парсит картинки в случае отсутствия
        elif today_is_wednesday() and path_to_zhabka != '':
            image_from_pc = FSInputFile(path_to_zhabka)
            await message.answer_photo(
                image_from_pc
            )
            delete_file(path_to_zhabka)
        else:
            path_to_zhabka = get_random_image('no_wednesday')
            image_from_pc = FSInputFile(path_to_zhabka)
            await message.answer_photo(
                image_from_pc
            )
            await message.answer(f'! Сегодня не среда !\n! Будь  бдительней !')
    else:
        await message.answer(f'Для чего вам картинка с жабой, если вы не подписаны?\n'
                             f'Все о подписке - /help')


async def change_subscribe(message: Message) -> None:
    """
    Обработчик команды вида /subscribe 1 или /subscribe 0
    /subscribe 1 - Подписка на рассылку
    /subscribe 0 - Отписка от рассылки

    :param message: Сообщение от пользователя.
    :type message: Message
    """
    split_message = message.text.split()
    if 3 > len(split_message) > 1:
        id_user = message.from_user.id
        chat_id = message.chat.id
        new_subscribe_status = split_message[-1] == '1'
        result_updates = await update_subscribe_status(user_id=id_user, new_subscribe_status=new_subscribe_status)
        if result_updates and new_subscribe_status:
            scheduled_time = datetime(2023, 12, 15, 12, 0, 0).time()
            await insert_schedule(chat_id=chat_id, user_id=id_user, scheduled_time=scheduled_time)
            await message.answer('Вы успешно подписались на ежесредную рассылку')
        elif result_updates and not new_subscribe_status:
            result_unsubscribe = await delete_schedule(chat_id=chat_id, user_id=id_user)
            if result_unsubscribe:
                await message.answer('Вы отписались от ежесредной рассылки')
            else:
                await message.answer('Не удалось отписаться, что-то пошло не так')
        else:
            await message.answer('Не удалось подписаться, что-то пошло не так')
    else:
        await message.answer('Вы не верно ввели команду.\n'
                             'Должно быть вида <code>/subscribe 1</code> или <code>/subscribe 0</code>')




# Админские команды
async def get_subscribe_command(message: Message) -> None:
    """
    Обработчик админской команды /subs.

    :param message: Сообщение от пользователя.
    :type message: Message
    """
    if message.from_user.id == settings.bots.id_admin:
        response_sub_users = "! Нет подписанных пользователей !"
        result_sub_users = await get_all_subscribed_users()
        if result_sub_users:
            response_sub_users = ''
            for i_string in result_sub_users:
                response_sub_users += f'''=====================================
User_id: <code>{i_string['user_id']}</code>
Username: <code>{i_string['username']}</code>
Subscribe: {i_string['subscribe']}
=====================================\n
'''
        await message.answer(response_sub_users)
    else:
        await message.answer("У вас нет прав для выполнения этой команды.")


async def get_update_pictures(message: Message) -> None:
    """
    Обработчик админской команды /updpic.

    :param message: Сообщение от пользователя.
    :type message: Message
    """
    if message.from_user.id == settings.bots.id_admin:
        await message.answer("! Апдейт картинок - Ожидайте !")
    else:
        await message.answer("У вас нет прав для выполнения этой команды.")


async def get_subscribe_time_command(message: Message) -> None:
    """
    Обработчик админской команды /time.

    :param message: Сообщение от пользователя.
    :type message: Message
    """
    if message.from_user.id == settings.bots.id_admin:
        response_sub_times = "! Нет записей о времени подписки! "
        result_sub_times = await get_all_time_data()
        if result_sub_times:
            response_sub_times = ''
            for i_string in result_sub_times:
                response_sub_times += f'''=====================================
Chat_id: <code>{i_string['chat_id']}</code>
User_id: <code>{i_string['user_id']}</code>
Время рассылки: {i_string['scheduled_time'].strftime('%H:%M')}
=====================================\n
'''
        await message.answer(response_sub_times)
    else:
        await message.answer("У вас нет прав для выполнения этой команды.")


async def restart_bot(message: Message) -> None:
    """
    Обработчик админской команды /restart

    :param message: Объект сообщения, который инициировал команду перезапуска.
    :type message: Message
    """
    if message.chat.id == settings.bots.id_admin:
        await message.answer("Перезапуск бота...")
