from core.parser.pic_parser import ya_updater
from core.states.st_loop import StateLoop


async def async_wrapper_parser() -> bool:
    """
    Асинхронная обертка синхронной функции,
    которая обновляет картинки.

    :return: True или False
    :rtype: bool
    """
    if await StateLoop.st_loop.run_in_executor(None, ya_updater):
        return True
    else:
        return False
