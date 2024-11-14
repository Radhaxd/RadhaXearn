
# UPI Giveaway Bot

This is a Telegram bot for managing referrals, UPI giveaways, and user engagement.

## Setup

1. Clone this repository
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory with the following content:
   ```
   API_ID=your_api_id
   API_HASH=your_api_hash
   BOT_TOKEN=your_bot_token
   MONGO_URI=your_mongodb_connection_string
   ```
4. Replace the placeholder values in the `.env` file with your actual credentials
5. Update the `ADMIN_USER_IDS` and `REQUIRED_CHANNELS` in `config.py`

## Running the Bot

To start the bot, run:
```
python main.py
```

## Features

- User registration and referral tracking
- Daily bonus system
- Leaderboard
- Admin commands for managing users and balances
- Withdrawal requests
- Task system
- User levels and XP
- Simple mini-game
- User profiles
- Shop system with inventory

## Admin Commands

- `/ban_user <user_id>`: Ban a user
- `/check_balance <user_id>`: Check a user's balance
- `/set_balance <user_id> <new_balance>`: Set a user's balance
- `/broadcast <message>`: Send a message to all users

## User Commands

- `/start`: Start the bot and get referral link
- `/balance`: Check current balance
- `/refer`: Get referral information
- `/leaderboard`: View top referrers
- `/withdraw`: Request a withdrawal
- `/bonus`: Claim daily bonus
- `/tasks`: View available tasks
- `/complete_task <task_id>`: Complete a task
- `/play`: Play a simple number guessing game
- `/profile`: View your user profile and inventory
- `/shop`: Browse available items in the shop
- `/buy <item_id>`: Purchase an item from the shop

## Contributing

Feel free to submit pull requests or open issues to improve the bot.

## License

This project is licensed under the MIT License.
