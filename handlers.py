
from pyrogram import filters
from config import REFERRAL_BONUS, MINIMUM_WITHDRAWAL
from database import (
    get_user, create_user, update_user_balance, 
    get_user_referrals, get_leaderboard, update_user_bonus_claim,
    add_xp, get_tasks, complete_task, get_shop_items, purchase_item, get_user_inventory,
    get_daily_quests, complete_quest, update_quest_progress
)
from utils import check_user_joined_channels, generate_referral_link
from datetime import datetime, timedelta
import random

def register_handlers(app):
    @app.on_message(filters.command("start"))
    async def start_command(client, message):
        user_id = message.from_user.id
        user = get_user(user_id)
        
        if not user:
            referrer_id = message.text.split()[-1] if len(message.text.split()) > 1 else None
            if referrer_id and referrer_id.isdigit() and int(referrer_id) != user_id:
                referrer = get_user(int(referrer_id))
                if referrer:
                    update_user_balance(referrer['user_id'], referrer['balance'] + REFERRAL_BONUS)
                    update_quest_progress(referrer['user_id'], 'referral', 1)
            
            create_user(user_id)
            user = get_user(user_id)
        
        if not check_user_joined_channels(client, user_id):
            # Prompt user to join required channels
            return
        
        referral_link = generate_referral_link(user_id)
        await message.reply_text(
            f"🏡 Welcome to UPI Giveaway Bot!\n\n"
            f"💰 Balance: ₹{user['balance']}\n"
            f"💰 Per Referral: ₹{REFERRAL_BONUS} UPI Cash\n"
            f"✨ Your Referral Link: {referral_link}\n\n"
            f"🏆 Your Level: {user['level']}\n"
            f"🌟 XP: {user['xp']}\n\n"
            "Share with friends and family to earn referral bonuses and grow your balance!"
        )

    @app.on_message(filters.command("profile"))
    async def profile_command(client, message):
        user_id = message.from_user.id
        user = get_user(user_id)
        referral_count = len(get_user_referrals(user_id))
        inventory = get_user_inventory(user_id)
        
        profile_text = (
            f"👤 User Profile\n\n"
            f"🆔 User ID: {user_id}\n"
            f"💰 Balance: ₹{user['balance']}\n"
            f"🏆 Level: {user['level']}\n"
            f"🌟 XP: {user['xp']}\n"
            f"👥 Referrals: {referral_count}\n"
            f"📅 Joined: {user['joined_date'].strftime('%Y-%m-%d')}\n\n"
            f"🎒 Inventory:\n"
        )
        
        if inventory:
            for item in inventory:
                profile_text += f"- {item}\n"
        else:
            profile_text += "Your inventory is empty.\n"
        
        profile_text += "\n🔮 Active Effects:\n"
        for effect, value in user['active_effects'].items():
            profile_text += f"- {effect}: {value}\n"
        
        await message.reply_text(profile_text)

    @app.on_message(filters.command("shop"))
    async def shop_command(client, message):
        shop_items = get_shop_items()
        shop_text = "🛍️ Welcome to the Shop!\n\n"
        
        for item in shop_items:
            shop_text += f"🏷️ {item['name']} - ₹{item['price']}\n"
            shop_text += f"   {item['description']}\n"
            shop_text += f"   Effect: {item['effect']} (+{item['effect_value']})\n\n"
        
        shop_text += "To purchase an item, use /buy <item_id>"
        await message.reply_text(shop_text)

    @app.on_message(filters.command("buy"))
    async def buy_command(client, message):
        user_id = message.from_user.id
        item_id = message.text.split()[-1]
        
        if purchase_item(user_id, item_id):
            update_quest_progress(user_id, 'purchase', 1)
            await message.reply_text("Item purchased successfully! Check your inventory with /profile")
        else:
            await message.reply_text("Purchase failed. Make sure you have enough balance and the item ID is correct.")

    @app.on_message(filters.command("quests"))
    async def quests_command(client, message):
        user_id = message.from_user.id
        quests = get_daily_quests(user_id)
        
        quests_text = "📋 Daily Quests:\n\n"
        for quest in quests:
            progress = quest.get('progress', 0)
            quests_text += f"🎯 {quest['name']}\n"
            quests_text += f"   {quest['description']}\n"
            quests_text += f"   Progress: {progress}/{quest['goal']}\n"
            quests_text += f"   Reward: ₹{quest['reward']}\n\n"
        
        quests_text += "Quests are automatically completed when you reach the goal."
        await message.reply_text(quests_text)

    @app.on_message(filters.command("play"))
    async def play_game_command(client, message):
        user_id = message.from_user.id
        user = get_user(user_id)
        
        # Simple number guessing game
        number = random.randint(1, 10)
        await message.reply_text("I'm thinking of a number between 1 and 10. Can you guess it?")
        
        @app.on_message(filters.user(user_id) & filters.text)
        async def guess_handler(client, message):
            try:
                guess = int(message.text)
                if guess == number:
                    reward = random.randint(1, 5)
                    new_balance = user['balance'] + reward
                    update_user_balance(user_id, new_balance)
                    new_level = add_xp(user_id, 10)
                    update_quest_progress(user_id, 'game_win', 1)
                    await message.reply_text(f"Congratulations! You guessed correctly.\nYou've won ₹{reward} and 10 XP!\nYour new level is: {new_level}")
                else:
                    await message.reply_text(f"Sorry, that's not correct. The number was {number}. Try again!")
                app.remove_handler(guess_handler)
            except ValueError:
                await message.reply_text("Please enter a valid number between 1 and 10.")

    # Add more handlers as needed
