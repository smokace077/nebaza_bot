# bot.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio

TOKEN = "7927251921:AAHWATrztnIFIeflJ5uI-1lYVcc2IHuX4gg"

app = FastAPI()
telegram_app = ApplicationBuilder().token(TOKEN).build()

# === Хэндлер Telegram-команды /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Бот запущен и работает.")

telegram_app.add_handler(CommandHandler("start", start))


@app.get("/")
async def root():
    return {"message": "Hello, FastAPI is working!"}

@app.post("/process")
async def process_data(request: Request):
    data = await request.json()
    return JSONResponse(content={"received": data})

# === Хук запуска FastAPI ===
@app.on_event("startup")
async def startup_event():
    await telegram_app.initialize()
    await telegram_app.start()
    print("Telegram Bot started.")

# === Хук остановки FastAPI ===
@app.on_event("shutdown")
async def shutdown_event():
    await telegram_app.stop()
    await telegram_app.shutdown()
    print("Telegram Bot stopped.")


# Только для локального запуска (на Render используется Procfile)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("bot:app", host="0.0.0.0", port=8000)
