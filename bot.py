import logging
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# 👉 ВСТАВЛЕННЫЙ ТОКЕН
BOT_TOKEN = "7644687597:AAEmXG5dCMkEHkkR2OOcZ1ixPtXPJdA1sY4"

# Логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# FastAPI-приложение
app = FastAPI()

# Telegram-приложение
telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()


# Стартовая команда
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Бот работает 🚀")


# Роут от FastAPI — хук для Telegram webhook
@app.post("/webhook")
async def telegram_webhook(request: Request):
    update = await request.json()
    await telegram_app.process_update(Update.de_json(update, telegram_app.bot))
    return {"ok": True}


# Добавление хендлеров
telegram_app.add_handler(CommandHandler("start", start))


# Запуск Telegram-бота в фоне при старте FastAPI
@app.on_event("startup")
async def startup_event():
    # Устанавливаем webhook
    webhook_url = "https://nebaza-bot.onrender.com/webhook"
    await telegram_app.bot.set_webhook(webhook_url)
    # Запускаем telegram-приложение в фоне
    telegram_app.initialize()
    await telegram_app.start()
    await telegram_app.updater.start_polling()  # Необязателен, если только webhook


@app.on_event("shutdown")
async def shutdown_event():
    await telegram_app.updater.stop()
    await telegram_app.stop()
