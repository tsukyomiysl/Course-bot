from dotenv import load_dotenv
from aiogram import Bot , Dispatcher
import os

load_dotenv()
token = os.environ["BOT_TOKEN"]
admin_id = os.environ["ADMIN_ID"]



bot = Bot(token)
dp = Dispatcher()