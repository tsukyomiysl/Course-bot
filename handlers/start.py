from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

start_rout = Router()

@start_rout.message(Command("start"))
async def start_bot(message : Message):
    if message.from_user:
        await message.answer(f"Привет {message.from_user.full_name}!")