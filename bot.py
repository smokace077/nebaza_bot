import os
import logging
import tempfile
import asyncio
import openai
import httpx

from fastapi import FastAPI, Request
from telegram import Update, Voice
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from pydub import AudioSegment

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

logging.basicConfig(level=logging.INFO)
app = FastAPI()

telegram_app = Application.builder().token(TOKEN).build()


async def transcribe(voice_file_path: str) -> str:
    audio = AudioSegment.from_ogg(voice_file_path)
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as mp3_file:
        audio.export(mp3_file.name, format="mp3")
        mp3_file_path = mp3_file.name

    with open(mp3_file_path, "rb") as f:
        transcript = openai.Audio.transcribe("whisper-1", f)
        return transcript["text"]


async def chatgpt_response(prompt: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


async def generate_voice(text: str) -> str:
    speech_response = openai.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=text
    )
    file_path = tempfile.mktemp(suffix=".mp3")
    with open(file_path, "wb") as f:
        f.write(speech_response.content)
    return file_path


@telegram_app.post_init
async def on_start(app: Application) -> None:
    webhook_url = os.getenv("RENDER_EXTERNAL_URL") + "/webhook"
    await app.bot.set_webhook(webhook_url)


@telegram_app.get("/")
async def root(request: Request):
    return {"status": "ok"}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Привет! Отправь голосовое сообщение, и я отвечу голосом.")


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    voice: Voice = update.message.voice
    file = await context.bot.get_file(voice.file_id)

    with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as f:
        voice_path = f.name
        await file.download_to_drive(f.name)

    transcribed_text = await transcribe(voice_path)
    reply_text = await chatgpt_response(transcribed_text)
    tts_path = await generate_voice(reply_text)

    await context.bot.send_voice(chat_id=update.effective_chat.id, voice=open(tts_path, "rb"))


telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(MessageHandler(filters.VOICE, handle_voice))

@app.post("/webhook")
async def telegram_webhook(req: Request):
    data = await req.json()
    await telegram_app.update_queue.put(Update.de_json(data, telegram_app.bot))
    return {"ok": True}
