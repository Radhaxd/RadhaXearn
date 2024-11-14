
from pymongo import MongoClient
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client['refer_earn_bot']
quests_collection = db['quests']

initial_quests = [
    {
        "name": "Referral Master",
        "description": "Refer 3 new users to the bot",
        "reward": 50,
        "type": "referral",
        "goal": 3
    },
    {
        "name": "XP Grinder",
        "description": "Earn 100 XP",
        "reward": 30,
        "type": "xp",
        "goal": 100
    },
    {
        "name": "Shop Enthusiast",
        "description": "Purchase an item from the shop",
        "reward": 25,
        "type": "purchase",
        "goal": 1
    },
    {
        "name": "Mini-game Champion",
        "description": "Win the number guessing game 3 times",
        "reward": 40,
        "type": "game_win",
        "goal": 3
    },
    {
        "name": "Daily Bonus Streak",
        "description": "Claim your daily bonus 5 days in a row",
        "reward": 60,
        "type": "bonus_streak",
        "goal": 5
    }
]

def init_quests():
    quests_collection.delete_many({})  # Clear existing quests
    quests_collection.insert_many(initial_quests)
    print(f"{len(initial_quests)} quests added to the database.")

if __name__ == "__main__":
    init_quests()
