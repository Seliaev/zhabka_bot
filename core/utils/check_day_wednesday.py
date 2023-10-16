from dateutil.parser import parse
from datetime import datetime


def today_is_wednesday() -> bool:
    """
    Проверяет, является ли текущий день средой.

    :return: True, если текущий день - среда, иначе False.
    :rtype: Bool
    """
    today_day = str(datetime.now().today().date())
    date = parse(today_day, dayfirst=True, yearfirst=True, fuzzy=True)
    return date.weekday() == 2
