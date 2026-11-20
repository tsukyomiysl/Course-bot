from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, LabeledPrice
from aiogram.filters import Command
from handlers.kb import get_kb
from models.buy_class import BuyData
from models.agent import c_agent
from product import PRODUCT
from models.payload import Payload
from config import bot




buy_router = Router()


@buy_router.message(Command('buy'))
async def get_course(message : Message):
    if message.from_user:
        await message.answer(
            f"""Название :{PRODUCT.title}
    Описание : {PRODUCT.description},
    Цена : {PRODUCT.price} ⭐
            """,
            reply_markup=get_kb(message.from_user.id, PRODUCT.id)
        )


@buy_router.callback_query(BuyData.filter(F.action == "no"))
async def get_refusal(query : CallbackQuery, callback_data : BuyData):
    await query.answer("Покупка отменена")
    if query.message:
        await query.message.edit_text("Отменено")
    

@buy_router.callback_query(BuyData.filter(F.action == "yes"))
async def get_agree(query : CallbackQuery, callback_data : BuyData):
    user_id = query.from_user.id
    if user_id != callback_data.user_id:
        await query.answer("Покупка может быть произведена только пользователем, запросившим оплату")
        return 
    
    if await c_agent.get_confirm(user_id) and query.message:
        await query.message.answer("У вас уже куплен данный товар , получите его через /get")
        return
    payload = (Payload(user_id=callback_data.user_id,item_id=callback_data.item_id)).pack()
    if query.message:
        await query.message.answer_invoice(
            title=PRODUCT.title,
            description=PRODUCT.description,
            payload=payload,
            currency="XTR",
            prices=[LabeledPrice(label="оплата товара", amount=PRODUCT.price)],
            provider_token="",

        )

@buy_router.message(F.successful_payment)
async def get_paid(message : Message):
    pay_data = message.successful_payment
    payload = Payload.unpack(pay_data.invoice_payload)
    charge_id = pay_data.telegram_payment_charge_id
    result = await c_agent.add_confirm(payload.user_id, payload.item_id, charge_id)
    if result:
        await message.answer("✅ Оплата прошла успешно , для получения товара воспользуйтесь командой /get")
    else:
        await bot.refund_star_payment(user_id=payload.user_id, telegram_payment_charge_id=charge_id)
        await message.answer("🔄 Произошла ошибка , возврат средств осуществлен")