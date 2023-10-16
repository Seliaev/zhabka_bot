import os
import random


def get_random_image(second_folder: str) -> str:
    """
    Выбирает и возвращает случайную картинку из папки с изображениями.

    :return: Путь к выбранной случайной картинке.
    :rtype: Str
    """
    current_dir = os.getcwd()
    first_folder = 'images'
    path_folder = os.path.join(current_dir, first_folder, second_folder)
    images = os.listdir(path_folder)

    if images:
        random_image = random.choice(images)
        image_path = os.path.join(path_folder, random_image)
        return image_path
    else:
        return ""  # Если нет доступных изображений, возвращаем пустую строку


def delete_file(file_path: str):
    """
    Удаляет файл по указанному пути.

    :param file_path: Путь к файлу, который нужно удалить.
    """
    os.remove(file_path)

