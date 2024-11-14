
from pyrogram import filters
from database import (
    get_user, create_user, update_user_balance, 
    get_user_referrals, get_leaderboard
)
from utils import check_user_joined_channels, generate_referral_link

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
            f"🏡 Welcome to UPI Giveaway Bot!

"
            f"💰 Balance: ₹{user['balance']}
"
            f"💰 Per Referral: ₹{REFERRAL_BONUS} UPI Cash
"
            f"✨ Your Referral Link: {referral_link}

"
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
            f"💰 Per Refer: ₹{REFERRAL_BONUS} UPI Cash

"
            f"👤 Your Referral Link: {referral_link}

"
            f"You have referred: {referral_count} users who have joined successfully."
        )

    @app.on_message(filters.command("leaderboard"))
    async def leaderboard_command(client, message):
        leaderboard = get_leaderboard()
        leaderboard_text = "😍 Top Users with Most Refers:

"
        
        for i, user in enumerate(leaderboard[:10], 1):
            leaderboard_text += f"{i}. User ID: {user['user_id']}, Referrals: {user['referral_count']}
"
        
        await message.reply_text(leaderboard_text)

    # Add more handlers for withdraw, bonus, etc.
