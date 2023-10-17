import asyncpg

from typing import Optional

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import Column, Integer, String, MetaData, Table, Boolean, \
    DateTime, func, ForeignKey, TIME, BigInteger
from core.settings import settings

# Параметры для подключения к базе данных
db_params = {
    "host": settings.db.host,
    "database": settings.db.database,
    "user": settings.db.username_database,
    "password": settings.db.password_database
}
# URL для подключения к базе данных
DATABASE_URL = (f"postgresql+asyncpg://{db_params['user']}:{db_params['password']}@"
                f"{db_params['host']}/{db_params['database']}")
engine = create_async_engine(DATABASE_URL, echo=True)

metadata = MetaData()
# Таблица для хранения данных пользователей
users = Table(
    'users', metadata,
    Column('user_id', Integer, primary_key=True),  # Уникальный идентификатор пользователя телеграм
    Column('username', String, nullable=True, default=None),  # Имя пользователя (может быть пустым)
    Column('subscribe', Boolean, default=False),  # Флаг подписки пользователя (по умолчанию False)
    Column('reg_time', DateTime, server_default=func.now()),
    # Дата и время регистрации пользователя (по умолчанию текущее время)
    Column('upd_time', DateTime, onupdate=func.now(), server_default=func.now())
    # Дата и время последнего обновления информации о пользователе
)

# Таблица для хранения времени рассылки
schedules = Table(
    'schedules',
    metadata,
    Column('chat_id', BigInteger, primary_key=False, nullable=False), # Идентификатор чата с пользователем телеграм
    Column('user_id', Integer, ForeignKey('users.user_id'), nullable=False), # Связка с таблицей users  на user_id
    Column('scheduled_time', TIME, nullable=False), # Время рассылки. Функция назначения времени пока не готово. Задел на будущее
)


async def connect_to_database() -> Optional[asyncpg.Connection] or None:
    """
    Устанавливает асинхронное соединение с базой данных.

    :return: Соединение с базой данных.
    :rtype: asyncpg.Connection, в случае ошибки None
    """
    try:
        conn = await asyncpg.connect(**db_params)
        return conn
    except:
        return None


async def create_table() -> None:
    """Создает таблицу 'users' в базе данных."""
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)


async def close_database_connection(conn: asyncpg.Connection) -> None:
    """
    Закрывает асинхронное соединение с базой данных.

    :param conn: Соединение с базой данных.
    :type conn: asyncpg.Connection
    """
    if conn:
        await conn.close()

