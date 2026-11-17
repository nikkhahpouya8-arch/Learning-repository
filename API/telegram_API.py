from telegram import Bot
from decouple import config

BOT_TOKEN = config("BOT_TOKEN")

async def send_telegram_message(chat_id, message):
    
    my_bot = Bot(token=BOT_TOKEN)
    
    await my_bot.send_message(chat_id= chat_id, text= message)