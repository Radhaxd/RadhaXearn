
from pyrogram import filters
from database import get_user, update_user_balance, get_leaderboard
from config import ADMIN_USER_IDS

def register_admin_handlers(app):
    @app.on_message(filters.command("ban_user") & filters.user(ADMIN_USER_IDS))
    async def ban_user(client, message):
        if len(message.command) != 2:
            await message.reply_text("Usage: /ban_user <user_id>")
            return

        user_id = int(message.command[1])
        user = get_user(user_id)
        if not user:
            await message.reply_text("User not found.")
            return

        # Implement ban logic here
        # For example, set a 'banned' field in the user document
        await message.reply_text(f"User {user_id} has been banned.")

    @app.on_message(filters.command("check_balance") & filters.user(ADMIN_USER_IDS))
    async def check_balance(client, message):
        if len(message.command) != 2:
            await message.reply_text("Usage: /check_balance <user_id>")
            return

        user_id = int(message.command[1])
        user = get_user(user_id)
        if not user:
            await message.reply_text("User not found.")
            return

        await message.reply_text(f"User {user_id} balance: ₹{user['balance']}")

    @app.on_message(filters.command("set_balance") & filters.user(ADMIN_USER_IDS))
    async def set_balance(client, message):
        if len(message.command) != 3:
            await message.reply_text("Usage: /set_balance <user_id> <new_balance>")
            return

        user_id = int(message.command[1])
        new_balance = float(message.command[2])
        user = get_user(user_id)
        if not user:
            await message.reply_text("User not found.")
            return

        update_user_balance(user_id, new_balance)
        await message.reply_text(f"User {user_id} balance updated to ₹{new_balance}")

    @app.on_message(filters.command("broadcast") & filters.user(ADMIN_USER_IDS))
    async def broadcast(client, message):
        if len(message.command) < 2:
            await message.reply_text("Usage: /broadcast <message>")
            return

        broadcast_message = " ".join(message.command[1:])
        # Implement broadcasting logic here
        # For example, send the message to all users in the database
        await message.reply_text("Broadcast message sent successfully.")

    # Add more admin handlers as needed
