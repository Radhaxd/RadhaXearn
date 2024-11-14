
from pyrogram import filters
from config import REFERRAL_BONUS, MINIMUM_WITHDRAWAL
from database import (
    get_user, create_user, update_user_balance, 
    get_user_referrals, get_leaderboard, update_user_bonus_claim,
    add_xp, get_tasks, complete_task, get_shop_items, purchase_item, get_user_inventory,
    get_daily_quests, complete_quest
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
            await message.reply_text("Item purchased successfully! Check your inventory with /profile")
        else:
            await message.reply_text("Purchase failed. Make sure you have enough balance and the item ID is correct.")

    @app.on_message(filters.command("quests"))
    async def quests_command(client, message):
        user_id = message.from_user.id
        quests = get_daily_quests(user_id)
        
        quests_text = "📋 Daily Quests:\n\n"
        for quest in quests:
            quests_text += f"🎯 {quest['name']}\n"
            quests_text += f"   {quest['description']}\n"
            quests_text += f"   Reward: ₹{quest['reward']}\n\n"
        
        quests_text += "Complete a quest using /complete_quest <quest_id>"
        await message.reply_text(quests_text)

    @app.on_message(filters.command("complete_quest"))
    async def complete_quest_command(client, message):
        user_id = message.from_user.id
        quest_id = message.text.split()[-1]
        
        if complete_quest(user_id, quest_id):
            await message.reply_text("Quest completed successfully! Your reward has been added to your balance.")
        else:
            await message.reply_text("Failed to complete the quest. Make sure the quest ID is correct and you haven't already completed it.")

    # ... (keep all other existing handlers)

    # Add more handlers as needed
