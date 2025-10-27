import telebot
from youtubesearchpython import VideosSearch
import yt_dlp
import os

import logging
logging.basicConfig(level=logging.INFO)

TOKEN = os.environ.get("BOT_TOKEN")  # we’ll add this as env variable
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(msg):
    bot.reply_to(msg, "🎵 Send a song name and I’ll find it for you!")

@bot.message_handler(func=lambda m: True)
def music(msg):
    query = msg.text
    bot.reply_to(msg, f"Searching for: {query} 🔍")

    try:
        search = VideosSearch(query, limit=1)
        result = search.result()['result'][0]
        link = result['link']

        ydl_opts = {'format': 'bestaudio', 'outtmpl': 'song.mp3'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])

        bot.send_audio(msg.chat.id, open('song.mp3', 'rb'))
        os.remove('song.mp3')
    except Exception as e:
        bot.reply_to(msg, "❌ Error fetching song.")
        print(e)

bot.polling()
