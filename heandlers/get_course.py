from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from models.agent import c_agent
from product import PRODUCT


get_rout = Router()

@get_rout.message(Command("get"))
async def get_check(message : Message):
    if message.from_user:
        result = await c_agent.get_confirm(message.from_user.id)
    if result:
        await message.answer(f"""🗒 Название : {PRODUCT.title}
📖 Teкст :
- {PRODUCT.text}""")
    else:
        await message.answer("🙅Оплата товара не подтверждена")