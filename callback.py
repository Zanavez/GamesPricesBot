from aiogram.filters.callback_data import CallbackData


class GameCallbackFactory(CallbackData, prefix="game"):
    action: str
    id: int | None = None


class Pagination(CallbackData, prefix='pag'):
    action: str
    page: int
