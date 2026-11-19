from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from models.buy_class import BuyData

def get_kb(user_id, item_id):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
            InlineKeyboardButton(
                text="✅Подтвердить",
                callback_data=BuyData(action="yes",user_id=user_id, item_id=item_id).pack()
            ),
            InlineKeyboardButton(
                text="❌Отменить",
                callback_data=BuyData(action="no", user_id=user_id, item_id=item_id).pack()
            )

            ]
        ]
    )
    return kb