from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from models.agent import c_agent
from product import PRODUCT


get_router = Router()

@get_router.message(Command("get"))
async def get_check(message : Message):
    if message.from_user:
        result = await c_agent.get_confirm(message.from_user.id)
    else:
        await message.answer("Нехватка данных для обработки")
    if result:
        await message.answer(f"""🗒 Название : {PRODUCT.title}
📖 Teкст :
- {PRODUCT.text}""")
    else:
        await message.answer("🙅Оплата товара не подтверждена")