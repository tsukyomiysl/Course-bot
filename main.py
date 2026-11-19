from config import dp , bot
import asyncio
from heandlers.start import start_rout
from heandlers.buy import buy_router
from heandlers.pre_check import check_rout
from heandlers.get_course import get_rout
from models.agent import c_agent

async def main():
    try:
        await c_agent.get_connection()
        dp.include_router(start_rout)
        dp.include_router(buy_router)
        dp.include_router(check_rout)
        dp.include_router(get_rout)
        await dp.start_polling(bot)
    finally:
        await c_agent.pool.close()

asyncio.run(main())