from fastapi import FastAPI, Request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler
import json
import os

TOKEN = os.getenv("BOT_TOKEN", "7927251921:AAHWATrztnIFIeflJ5uI-1lYVcc2IHuX4gg")

app = FastAPI()
telegram_bot = Bot(token=TOKEN)
dispatcher = Dispatcher(telegram_bot, None, use_context=True)


# Обработчик команды /start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Бот работает.")


# Регистрируем обработчик
dispatcher.add_handler(CommandHandler("start", start))


# Вебхук от Telegram
@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.body()
    update = Update.de_json(json.loads(data.decode("utf-8")), telegram_bot)
    dispatcher.process_update(update)
    return {"ok": True}


# Главная страница для проверки (GET-запросы)
@app.get("/")
async def root():
    return {"message": "Бот работает. Используй /webhook для Telegram."}


# Установка вебхука при старте
@app.on_event("startup")
async def on_startup():
    webhook_url = "https://nebaza-bot.onrender.com/webhook"
    await telegram_bot.set_webhook(webhook_url)
    print(f"✅ Webhook установлен: {webhook_url}")
