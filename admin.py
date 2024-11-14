
from pyrogram import filters
from database import get_user, update_user_balance, get_leaderboard, get_shop_items, get_tasks, quests_collection, shop_items_collection
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

    @app.on_message(filters.command("add_quest") & filters.user(ADMIN_USER_IDS))
    async def add_quest(client, message):
        if len(message.command) < 6:
            await message.reply_text("Usage: /add_quest <name> <description> <reward> <type> <goal>")
            return

        name = message.command[1]
        description = " ".join(message.command[2:-3])
        reward = int(message.command[-3])
        quest_type = message.command[-2]
        goal = int(message.command[-1])

        new_quest = {
            "name": name,
            "description": description,
            "reward": reward,
            "type": quest_type,
            "goal": goal
        }

        quests_collection.insert_one(new_quest)
        await message.reply_text("New quest added successfully.")

    @app.on_message(filters.command("remove_quest") & filters.user(ADMIN_USER_IDS))
    async def remove_quest(client, message):
        if len(message.command) != 2:
            await message.reply_text("Usage: /remove_quest <quest_id>")
            return

        quest_id = message.command[1]
        result = quests_collection.delete_one({"_id": quest_id})

        if result.deleted_count > 0:
            await message.reply_text("Quest removed successfully.")
        else:
            await message.reply_text("Quest not found.")

    @app.on_message(filters.command("add_shop_item") & filters.user(ADMIN_USER_IDS))
    async def add_shop_item(client, message):
        if len(message.command) < 6:
            await message.reply_text("Usage: /add_shop_item <name> <description> <price> <effect> <effect_value>")
            return

        name = message.command[1]
        description = " ".join(message.command[2:-3])
        price = int(message.command[-3])
        effect = message.command[-2]
        effect_value = float(message.command[-1])

        new_item = {
            "name": name,
            "description": description,
            "price": price,
            "effect": effect,
            "effect_value": effect_value
        }

        shop_items_collection.insert_one(new_item)
        await message.reply_text("New shop item added successfully.")

    @app.on_message(filters.command("remove_shop_item") & filters.user(ADMIN_USER_IDS))
    async def remove_shop_item(client, message):
        if len(message.command) != 2:
            await message.reply_text("Usage: /remove_shop_item <item_id>")
            return

        item_id = message.command[1]
        result = shop_items_collection.delete_one({"_id": item_id})

        if result.deleted_count > 0:
            await message.reply_text("Shop item removed successfully.")
        else:
            await message.reply_text("Shop item not found.")

    # Add more admin handlers as needed
