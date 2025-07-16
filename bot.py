import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import os

API_TOKEN = os.getenv("API_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я твой Nebaza-бот. Задай вопрос.")

@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(f"Ты написал: {message.text}")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
