from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

TOKEN = "7927251921:AAHWATrztnIFIeflJ5uI-1lYVcc2IHuX4gg"
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://nebaza-bot.onrender.com{WEBHOOK_PATH}"

app = FastAPI()
telegram_app = ApplicationBuilder().token(TOKEN).build()


# === Telegram handler ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Бот готов к работе.")


telegram_app.add_handler(CommandHandler("start", start))


@app.on_event("startup")
async def startup_event():
    await telegram_app.initialize()
    await telegram_app.start()
    await telegram_app.bot.set_webhook(WEBHOOK_URL)
    print("✅ Webhook установлен:", WEBHOOK_URL)


@app.on_event("shutdown")
async def shutdown_event():
    await telegram_app.bot.delete_webhook()
    await telegram_app.stop()
    await telegram_app.shutdown()
    print("🛑 Webhook удалён и бот остановлен")


@app.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    data = await request.body()
    update = Update.de_json(data.decode("utf-8"), telegram_app.bot)
    await telegram_app.process_update(update)
    return {"status": "ok"}


@app.get("/")
async def root():
    return {"message": "FastAPI + Telegram Webhook работает"}
