from config import dp , bot
import asyncio
from handlers.start import start_rout
from handlers.buy import buy_router
from handlers.pre_check import pre_check_router
from handlers.get_course import get_router
from models.agent import c_agent

async def main():
    try:
        await c_agent.get_connection()
        dp.include_router(start_rout)
        dp.include_router(buy_router)
        dp.include_router(pre_check_router)
        dp.include_router(get_router)
        await dp.start_polling(bot)
    finally:
        await c_agent.pool.close()

asyncio.run(main())