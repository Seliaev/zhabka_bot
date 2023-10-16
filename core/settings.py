import os

from environs import Env
from dataclasses import dataclass


@dataclass
class Bots:
    """Класс для хранения настроек бота."""
    bot_token: str
    id_admin: int


@dataclass
class DataBase:
    """Класс для хранения настроек БД."""
    host: str
    database: str
    username_database: str
    password_database: str


@dataclass
class Settings:
    """Класс для хранения всех настроек."""
    bots: Bots
    db: DataBase


def get_settings(path: str) -> Settings:
    """
    Получает настройки из файла .env.

    :param path: Путь к файлу .env.
    :type path: str

    :return: Настройки бота и БД.
    :rtype: Settings
    """
    env = Env()
    env.read_env(path)

    return Settings(
        bots=Bots(
            bot_token=env.str('TOKEN'),
            id_admin=env.int('ID_ADMIN')
        ),
        db=DataBase(
            host=env.str('HOST'),
            database=env.str('DATABASE'),
            username_database=env.str('USERNAME_DATABASE'),
            password_database=env.str('PASSWORD_DATABASE')
        )
    )


root_path = os.getcwd()
env_file_path = os.path.join(root_path, '.env')
settings = get_settings(env_file_path)

