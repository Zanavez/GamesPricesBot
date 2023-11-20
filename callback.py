from aiogram.filters.callback_data import CallbackData


class GameCallbackFactory(CallbackData, prefix="game"):
    action: str
    id: int | None = None
