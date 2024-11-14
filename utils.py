
from pyrogram.errors import UserNotParticipant
from config import REQUIRED_CHANNELS

def check_user_joined_channels(client, user_id):
    for channel in REQUIRED_CHANNELS:
        try:
            client.get_chat_member(channel, user_id)
        except UserNotParticipant:
            return False
    return True

def generate_referral_link(user_id):
    bot_username = "your_bot_username"  # Replace with your bot's username
    return f"https://t.me/{bot_username}?start={user_id}"

# Add more utility functions as needed
