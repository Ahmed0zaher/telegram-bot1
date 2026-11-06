import random
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

@app.on_message(filters.text & ~filters.command(["start"]))
def download_media(client, message):
    url = message.text.strip()
    
    if not url.startswith("http://") and not url.startswith("https://"):
        return

    msg = message.reply_text("جاري تحميل الميديا، يرجى الانتظار قليلاً...")
    random_filename = f"media_{random.randint(1000, 9999)}"
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': f'{random_filename}.%(ext)s',
        'quiet': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
        if "spotify.com" in url:
            message.reply_audio(filename)
        else:
            message.reply_video(filename)
            
        msg.delete()
        
        if os.path.exists(filename):
            os.remove(filename)
            
    except Exception as e:
        msg.edit_text("❌ عذراً، لقد قمت بأرسال رابط غير صحيح")
        for f in os.listdir('.'):
            if f.startswith(random_filename):
                os.path.exists(f) and os.remove(f)
app.run()
