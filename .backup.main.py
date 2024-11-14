
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
from handlers import register_handlers
from admin import register_admin_handlers

app = Client("refer_earn_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

if __name__ == "__main__":
    register_handlers(app)
    register_admin_handlers(app)
    print("Bot is starting...")
    app.run()
