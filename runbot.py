import aiohttp
import os
from aiotg import Bot

bot = Bot(api_token=os.getenv("TELEGRAM_TOKEN"))

@bot.command("start")
async def start(chat, match):
    await chat.send_text("hello")

bot.run()
