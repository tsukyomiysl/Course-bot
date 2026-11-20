from aiogram.types import Message
from aiogram.types import PreCheckoutQuery
from aiogram import Router
from models.payload import PayLoad
from product import PRODUCT
from models.agent import c_agent
pre_check_router = Router()

@pre_check_router.pre_checkout_query()
async def check_query(query : PreCheckoutQuery):
    payload = PayLoad.unpack(query.invoice_payload)
    user_id = query.from_user.id
    curr = query.currency
    amount = query.total_amount
    if payload.user_id != user_id:
        await query.answer(ok=False, error_message="Счет сформирован другим пользователем")
        return
    if curr != "XTR":
        await query.answer(ok=False, error_message="Оплата производится сторонней валютой")
        return
    if PRODUCT.id != payload.item_id:
        await query.answer(ok=False, error_message="Неизвестный товар")
        return
    if PRODUCT.price != amount:
        await query.answer(ok=False, error_message="Сумма платежа не соответствует назначеной")
        return
    if await c_agent.get_confirm(user_id):
        await query.answer(ok=False, error_message="Товар уже был куплен ранее")
        return
    await query.answer(ok=True)

