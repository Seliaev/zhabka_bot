from datetime import datetime, time
from typing import Optional, Union, Dict, List

from sqlalchemy import select, insert

from core.database.base import engine, schedules


async def insert_schedule(chat_id: int, user_id: int, scheduled_time: time):
    """Вставляет новую запись в таблицу 'schedules'."""
    try:
        async with engine.begin() as conn:
            query = insert(schedules).values(chat_id=chat_id, user_id=user_id, scheduled_time=scheduled_time)
            await conn.execute(query)
            print("Запись в таблицу 'schedules' добавлена успешно.")
    except Exception as e:
        print('Ошибка при вставке данных в таблицу schedules:', e)


async def get_subscription_time(user_id: int) -> List[datetime] or None:
    """Получает время подписки пользователя."""
    try:
        async with engine.begin() as conn:
            query = select([schedules.c.scheduled_time]).where(schedules.c.user_id == user_id)
            result = await conn.execute(query)
            subscription_times = [row[0] for row in result.fetchall()]
            return subscription_times
    except Exception as e:
        print('Ошибка при получении времени подписки:', e)
        return None


async def get_all_time_data() -> Optional[List[Dict[str, Union[int, str, bool]]]] or None:
    """
    !!!ДЛЯ ОТЛАДКИ!!!

    Получает данные всех пользователей из таблицы 'users'.

    :return: Возвращает список со словарями пользоваетльских данных.
                Внутри словарей: {'user_id':id телеграмм пользователя,
                                             'username': имя пользователя,
                                             'subscribe': наличие подписки}
    :rtype: List[dict], в случае ошибки None
    """
    try:
        async with engine.begin() as conn:
            query = schedules.select()
            result = await conn.execute(query)
            user_data = [
                {'chat_id': row[0], 'user_id': row[1], 'scheduled_time': row[2]}
                for row in result.fetchall()
            ]
            return user_data if user_data else []
    except Exception as e:
        print('Ошибка при получении данных из таблицы:', e)
        return None


async def delete_schedule(chat_id: int, user_id: int) -> bool:
    """Удаляет запись из таблицы 'schedules' по chat_id и user_id."""
    try:
        async with engine.begin() as conn:
            query = schedules.delete().where(
                (schedules.c.chat_id == chat_id) & (schedules.c.user_id == user_id)
            )
            result = await conn.execute(query)
            return bool(result.rowcount)  # Возвращает True, если запись была удалена
    except Exception as e:
        print('Ошибка при удалении записи из таблицы schedules:', e)
        return False
