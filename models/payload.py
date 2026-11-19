from aiogram.filters.callback_data import CallbackData
class PayLoad(CallbackData, prefix="pay"):
    user_id : int
    item_id : int