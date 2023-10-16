from aiogram import Bot
from aiogram.types import FSInputFile

from core.utils.check_day_wednesday import today_is_wednesday
from core.utils.photo_zhabka import get_random_image


async def send_zhabka_subscriber(bot: Bot, chat_id: int) -> None:
    """
    Отправляет случайное изображение по расписанию, в среду, в 12:00.
    По списку подписанных пользователей

    :param bot: Инстанс бота.
    :type bot: Bot
    :param chat_id: Идентификатор чата, в который нужно отправить изображение.
    :type chat_id: int
    """
    if today_is_wednesday():
        path_to_zhabka = get_random_image('wednesday')
        image_from_pc = FSInputFile(path_to_zhabka)
        await bot.send_photo(
            chat_id=chat_id,
            photo=image_from_pc
        )

