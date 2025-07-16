from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, ContextTypes
)
import logging

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Твой токен
BOT_TOKEN = "7644687597:AAEmXG5dCMkEHkkR2OOcZ1ixPtXPJdA1sY4"

# Создаём FastAPI приложение
app = FastAPI()

# Создаём Telegram-приложение
telegram_app = Application.builder().token(BOT_TOKEN).build()

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот успешно запущен через Render!")

# Регистрируем обработчик
telegram_app.add_handler(CommandHandler("start", start))

# FastAPI эндпоинт для Telegram webhook
@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)
    return {"ok": True}

# Устанавливаем webhook и запускаем Telegram приложение
@app.on_event("startup")
async def startup_event():
    webhook_url = "https://nebaza-bot.onrender.com/webhook"
    await telegram_app.bot.set_webhook(webhook_url)
    await telegram_app.initialize()
    await telegram_app.start()
