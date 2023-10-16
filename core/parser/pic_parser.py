"""
Синхронный модуль парсинга изображений с яндекс.картинок.

:return: True, если обновление прошло успешно, иначе False.
:rtype: bool
"""

import requests
import os
import time

from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import List
from random import randint, choice
from fake_headers import Headers


# header = Headers(
#     browser="chrome",  # Generate only Chrome UA
#     os="win",  # Generate ony Windows platform
#     headers=True  # generate misc headers
# )   - На случай фейковых, рандомных headers
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}

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


def parse_yandex_images(query: str = choice(querys), start_page: int = randint(0, 3),
                        limit: int = randint(20, 40)) -> List[str] or False:
    """
    Парсинг страницы Яндекс.Картинок и получение ссылок на изображения.

    :param query: Запрос для поиска изображений.
    :param start_page: Начальная страница для поиска.
    :param limit: Максимальное количество изображений для получения.
    :return: Список ссылок на изображения или False в случае ошибки.
    :rtype: List[str], при неудаче False
    """
    try:
        image_urls = []
        url = f"https://yandex.ru/images/search?text={query}&p={start_page}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        captcha_form = soup.select('#checkbox-captcha-form')
        if captcha_form:
            return False
        while len(image_urls) < limit:
            images = soup.select('.serp-item__thumb')
            for image in images:
                image_url = image['src']
                if not image_url.startswith('https://'):
                    image_url = urljoin(url, image_url)
                image_urls.append(image_url)
                if len(image_urls) >= limit:
                    break
            start_page += 1
        return image_urls[:limit]
    except:
        return False


def download_images(image_urls) -> bool:
    """
    Загрузка изображений по ссылкам в каталог.

    :param image_urls: Список ссылок на изображения для загрузки.
    :return: True, если загрузка прошла успешно, иначе False.
    :rtype: Bool
    """
    try:
        current_dir = os.getcwd()
        first_folder = 'images'
        second_folder = "wednesday"
        save_folder = os.path.join(current_dir, first_folder, second_folder)
        os.makedirs(save_folder, exist_ok=True)
        for i, url in enumerate(image_urls):
            time.sleep(0.3)
            response = requests.get(url)
            response.raise_for_status()
            file_path = os.path.join(save_folder, f"image_{i + 1}.jpg")
            with open(file_path, 'wb') as file:
                file.write(response.content)
        return True
    except:
        return False


def ya_updater() -> bool:
    """
    Обновление изображений с Яндекс.Картинок.

    :return: True, если обновление прошло успешно, иначе False.
    :rtype: bool
    """
    image_urls = parse_yandex_images()
    images = False
    if image_urls:
        images = download_images(image_urls)
    if images:
        return True
    else:
        return False