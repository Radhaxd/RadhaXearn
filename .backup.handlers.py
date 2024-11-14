
from pyrogram import filters
from config import REFERRAL_BONUS, MINIMUM_WITHDRAWAL
from database import (
    get_user, create_user, update_user_balance, 
    get_user_referrals, get_leaderboard, update_user_bonus_claim
)
from utils import check_user_joined_channels, generate_referral_link
from datetime import datetime, timedelta

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
            "Share with friends and family to earn referral bonuses and grow your balance!"
        )

    @app.on_message(filters.command("balance"))
    async def balance_command(client, message):
        user_id = message.from_user.id
        user = get_user(user_id)
        await message.reply_text(f"Your current balance is: ₹{user['balance']}")

    @app.on_message(filters.command("refer"))
    async def refer_command(client, message):
        user_id = message.from_user.id
        referral_link = generate_referral_link(user_id)
        referral_count = len(get_user_referrals(user_id))
        
        await message.reply_text(
            f"💰 Per Refer: ₹{REFERRAL_BONUS} UPI Cash\n\n"
            f"👤 Your Referral Link: {referral_link}\n\n"
            f"You have referred: {referral_count} users who have joined successfully."
        )

    @app.on_message(filters.command("leaderboard"))
    async def leaderboard_command(client, message):
        leaderboard = get_leaderboard()
        leaderboard_text = "😍 Top Users with Most Refers:\n\n"
        
        for i, user in enumerate(leaderboard[:10], 1):
            leaderboard_text += f"{i}. User ID: {user['user_id']}, Referrals: {user['referral_count']}\n"
        
        await message.reply_text(leaderboard_text)

    @app.on_message(filters.command("withdraw"))
    async def withdraw_command(client, message):
        user_id = message.from_user.id
        user = get_user(user_id)
        
        if user['balance'] < MINIMUM_WITHDRAWAL:
            await message.reply_text(f"You need a minimum balance of ₹{MINIMUM_WITHDRAWAL} to withdraw.")
            return
        
        # Here you would implement the actual withdrawal process
        # For now, we'll just simulate it
        update_user_balance(user_id, 0)  # Reset balance to 0 after withdrawal
        await message.reply_text(f"Withdrawal of ₹{user['balance']} processed successfully!")

    @app.on_message(filters.command("bonus"))
    async def bonus_command(client, message):
        user_id = message.from_user.id
        user = get_user(user_id)
        
        if 'last_bonus_claim' not in user or user['last_bonus_claim'].date() < datetime.now().date():
            bonus_amount = min(7, user.get('consecutive_bonus_days', 0) + 1)
            new_balance = user['balance'] + bonus_amount
            update_user_balance(user_id, new_balance)
            update_user_bonus_claim(user_id, bonus_amount)
            await message.reply_text(f"You've claimed your daily bonus of ₹{bonus_amount}!")
        else:
            time_until_next = timedelta(days=1) - (datetime.now() - user['last_bonus_claim'])
            await message.reply_text(f"You've already claimed your bonus today. Next bonus available in {time_until_next.seconds // 3600} hours.")

    # Add more handlers as needed
