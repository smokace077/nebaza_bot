# bot.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "7927251921:AAHWATrztnIFIeflJ5uI-1lYVcc2IHuX4gg"

app = FastAPI()

# Telegram команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Бот запущен и работает.")

# Запускаем Telegram Application отдельно
telegram_app = ApplicationBuilder().token(TOKEN).build()
telegram_app.add_handler(CommandHandler("start", start))

@app.get("/")
async def root():
    return {"message": "Hello, FastAPI is working!"}

@app.post("/process")
async def process_data(request: Request):
    data = await request.json()
    return JSONResponse(content={"received": data})

# Запуск бота как background task или отдельным процессом — простой вариант для Render:
import asyncio

@app.on_event("startup")
async def startup_event():
    # Запускаем Telegram бота в фоне
    asyncio.create_task(telegram_app.run_polling())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("bot:app", host="0.0.0.0", port=8000)
