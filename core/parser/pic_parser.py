"""
Синхронный модуль парсинга изображений с Google

:return: True, если обновление прошло успешно, иначе False.
:rtype: bool
"""

import os
from random import choice, randint
from datetime import datetime
from icrawler.builtin import GoogleImageCrawler

# Запросы для картинок
querys = ["it is wednesday my dude"
          "it's wednesday my dude",
          "it's wednesday",
          "wednesday - dudes",
          "Это среда мои чюваки",
          "Среда чюваки",
          "Средный день чюваки",
          "Лягушка мем среда"
          ]


def download_images() -> bool:
    """
    Загрузка изображений по запросу(из списка, рандомно) в каталог.

    :return: True, если загрузка прошла успешно, иначе False.
    :rtype: Bool
    """
    try:
        current_dir = os.getcwd()
        first_folder = 'images'
        second_folder = "wednesday"
        save_folder = os.path.join(current_dir, first_folder, second_folder)
        google_crawler = GoogleImageCrawler(storage={'root_dir': save_folder})
        google_crawler.crawl(keyword=choice(querys), max_num=randint(20, 50))
        return True
    except Exception as ex:
        with open('except_log_parser.log', 'a') as except_log:
            except_log.write(f"{datetime.now().strftime(format='%D - %H:%M')} | {ex}")
        return False


def ya_updater() -> bool:
    """
    Обновление изображений с Google.

    :return: True, если обновление прошло успешно, иначе False.
    :rtype: bool
    """
    result_crawl = download_images()
    return result_crawl
