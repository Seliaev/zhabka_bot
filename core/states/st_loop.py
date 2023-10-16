from aiogram.fsm.state import StatesGroup, State


class StateLoop(StatesGroup):
    """
    Устанавливает цикл событий
    """
    st_loop = State()
