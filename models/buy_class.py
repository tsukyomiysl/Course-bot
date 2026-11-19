from aiogram.filters.callback_data import CallbackData
class BuyData(CallbackData, prefix="buy"):
    action : str
    user_id : int
    item_id : int
