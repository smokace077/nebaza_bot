# bot.py
from fastapi import FastAPI
from telegram import Update, Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, filters
import asyncio

TOKEN = "7927251921:AAHWATrztnIFIeflJ5uI-1lYVcc2IHuX4gg"

app = FastAPI()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, update_queue=None, use_context=True)

# Обработчик команды /start
async def start(update: Update, context):
    await update.message.reply_text("Привет! Я бот на FastAPI")

# Эхо-обработчик: повторяет сообщение пользователя
async def echo(update: Update, context):
    await update.message.reply_text(f"Ты написал: {update.message.text}")

dp.add_handler(CommandHandler("start", start))
dp.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))

@app.on_event("startup")
async def startup_event():
    async def run_bot():
        offset = None
        while True:
            updates = await bot.get_updates(offset=offset, timeout=10)
            for update in updates:
                offset = update.update_id + 1
                dp.process_update(update)
            await asyncio.sleep(1)

    asyncio.create_task(run_bot())

@app.get("/")
async def root():
    return {"message": "Бот запущен и работает!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("bot:app", host="0.0.0.0", port=8000)
