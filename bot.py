import asyncio
import sys

if sys.version_info >= (3, 10):
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        except Exception:
            pass
import os
from pyrogram import Client, filters
import yt_dlp

TOKEN = "8946850480:AAE8siyU_MQjZT31d0e_a5C0ZJkdFAl9_k8"
app = Client(
    "social_bot",
    api_id=37636816,
    api_hash="e91f56ab17aa0ffbf24a156b5855c829",
    bot_token=TOKEN
)

@app.on_message(filters.command("start"))
def start_command(client, message):
    message.reply_text("مرحباً بك في بوت التحميل !📥أرسل لي أي رابط وسأقوم بتحميله لك فوراً")

@app.on_message(filters.text & ~filters.command("start"))
def download_media(client, message):
    url = message.text
    if not url.startswith("http"):
        message.reply_text("Please send a valid link.")
        return
    
    msg = message.reply_text("Downloading media, please wait...")
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.mp4',
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        message.reply_video("video.mp4")
        msg.delete()
    except Exception as e:
        msg.edit_text("❌┇عذراً لقد قمت بأرسال رابط غير صحيح.")

app.run()