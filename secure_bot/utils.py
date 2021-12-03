from aiogram.dispatcher.filters.state import State, StatesGroup


class BotState(StatesGroup):
    """Класс состояний бота."""

    ADMIN = State()
    STATE_0 = State()

