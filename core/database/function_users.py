from typing import Optional, Union, Dict, List

from core.database.base import engine, users


async def insert_data_in_table(user_id: int, username: str, subscribe: bool) -> bool or None:
    """
    Добавляет данные пользователя в таблицу 'users'.

    :param user_id: id телеграмм пользователя.
    :type user_id: int
    :param username: Имя пользователя.
    :type username: str
    :param subscribe: Статус подписки на рассылку.
    :type subscribe: bool

    :return: Возвращает True в случае успешного добавления пользователя в БД,
            False если пользователь есть в БД. None если ошибка.
    :rtype: bool, в случае ошибки None
    """
    try:
        check_user = await check_user_id_in_db(user_id)  # Проверка наличия пользователя в БД
        if not check_user:
            async with engine.begin() as conn:
                await conn.execute(
                    users.insert()
                    .values(user_id=user_id, username=username, subscribe=subscribe))
                return True
        else:
            return False
    except:
        return None


async def get_data_from_user_id(user_id: int):
    """
    Получает данные пользователя по его user_id из таблицы 'users'.

    :param user_id: id телеграмм пользователя.
    :type user_id: int

    :return: Возвращает словарь: {'user_id':id телеграмм пользователя,
                                 'username': имя пользователя,
                                 'subscribe': наличие подписки}
    :rtype: dict, в случае ошибки None
    """
    try:
        async with engine.connect() as conn:
            query = users.select(
            ).where(users.c
                    .user_id == user_id
                    )
            result = await conn.execute(query)
            row = result.fetchone()
            user_data = {'user_id': row[0], 'username': row[1], 'subscribe': row[2]}
            return user_data
    except:
        return None


async def update_subscribe_status(user_id: int, new_subscribe_status: bool) -> True or None:
    """
    Обновляет статус подписки пользователя по его user_id в таблице 'users'.

    :param user_id: id телеграмм пользователя.
    :type user_id: int
    :param new_subscribe_status: Новый статус подписки
    :type new_subscribe_status: bool
    """
    try:
        #check_user = await check_user_id_in_db(user_id)
       # print(new_subscribe_status, user_id)
        async with engine.begin() as conn:
                query = (
                    users.update()
                    .where(users.c.user_id == user_id)
                    .values(subscribe=new_subscribe_status)
                )
                await conn.execute(query)
                return True
    except:
        return None


async def get_all_subscribed_users() -> Optional[List[Dict[str, Union[int, str, bool]]]] or None:
    """
    !!!ДЛЯ ОТЛАДКИ!!!

    Получает данные всех пользователей, подписанных на рассылку, из таблицы 'users'.

    :return: Возвращает список со словарями пользоваетльских данных.
                Внутри словарей: {'user_id':id телеграмм пользователя,
                                             'username': имя пользователя,
                                             'subscribe': наличие подписки}
    :rtype: List[dict], в случае ошибки None
    """
    try:
        async with (engine.begin() as conn):
            query = users.select(
            ).where(users.c.
                    subscribe == True)
            result = await conn.execute(query)
            user_data = [
                {'user_id': row[0], 'username': row[1], 'subscribe': row[2]}
                for row in result.fetchall()
            ]
            return user_data if user_data else []
    except:
        return None


async def get_all_user_data() -> Optional[List[Dict[str, Union[int, str, bool]]]] or None:
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
            query = users.select()
            result = await conn.execute(query)
            user_data = [
                {'user_id': row[0], 'username': row[1], 'subscribe': row[2]}
                for row in result.fetchall()
            ]
            return user_data if user_data else []
    except:
        return None


async def check_user_id_in_db(user_id: int) -> List[Dict] or None:
    """
    Проверяет наличие пользователя в таблице 'users' по его user_id.

    :param user_id: id телеграмм пользователя.
    :type user_id: int

    :return: Возвразает список с одним элементом (словарь).
    Используется для проверки есть ли пользователь в БД.
    :rtype: List[dict], в случае ошибки None
    """
    try:
        async with engine.connect() as conn:
            query = users.select(
            ).where(users.c
                    .user_id == user_id
                    )
            result = await conn.execute(query)
            return result.fetchall()
    except:
        return None
