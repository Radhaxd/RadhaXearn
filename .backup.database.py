
from pymongo import MongoClient
from datetime import datetime, timedelta
from config import MONGO_URI
import random

client = MongoClient(MONGO_URI)
db = client['refer_earn_bot']
users_collection = db['users']
tasks_collection = db['tasks']
shop_items_collection = db['shop_items']
quests_collection = db['quests']

def get_user(user_id):
    return users_collection.find_one({'user_id': user_id})

def create_user(user_id):
    user = {
        'user_id': user_id,
        'balance': 0,
        'referrals': [],
        'joined_date': datetime.now(),
        'last_bonus_claim': None,
        'consecutive_bonus_days': 0,
        'level': 1,
        'xp': 0,
        'completed_tasks': [],
        'inventory': [],
        'active_effects': {},
        'last_quest_refresh': None,
        'current_quests': []
    }
    users_collection.insert_one(user)

def update_user_balance(user_id, new_balance):
    users_collection.update_one(
        {'user_id': user_id},
        {'$set': {'balance': new_balance}}
    )

def get_user_referrals(user_id):
    return users_collection.find({'referred_by': user_id})

def get_leaderboard():
    pipeline = [
        {'$project': {'user_id': 1, 'referral_count': {'$size': '$referrals'}}},
        {'$sort': {'referral_count': -1}},
        {'$limit': 10}
    ]
    return list(users_collection.aggregate(pipeline))

def update_user_bonus_claim(user_id, bonus_amount):
    today = datetime.now().date()
    users_collection.update_one(
        {'user_id': user_id},
        {
            '$set': {
                'last_bonus_claim': datetime.now(),
                'consecutive_bonus_days': bonus_amount
            },
            '$inc': {'balance': bonus_amount}
        }
    )

def add_xp(user_id, xp_amount):
    user = get_user(user_id)
    xp_multiplier = user['active_effects'].get('xp_booster', 1)
    total_xp = xp_amount * xp_multiplier
    
    user = users_collection.find_one_and_update(
        {'user_id': user_id},
        {'$inc': {'xp': total_xp}},
        return_document=True
    )
    
    new_level = (user['xp'] // 100) + 1  # Level up every 100 XP
    if new_level > user['level']:
        users_collection.update_one(
            {'user_id': user_id},
            {'$set': {'level': new_level}}
        )
    
    return new_level, total_xp

def get_tasks():
    return list(tasks_collection.find())

def complete_task(user_id, task_id):
    users_collection.update_one(
        {'user_id': user_id},
        {'$addToSet': {'completed_tasks': task_id}}
    )

def get_shop_items():
    return list(shop_items_collection.find())

def purchase_item(user_id, item_id):
    item = shop_items_collection.find_one({'_id': item_id})
    user = get_user(user_id)
    
    if not item or user['balance'] < item['price']:
        return False
    
    users_collection.update_one(
        {'user_id': user_id},
        {
            '$inc': {'balance': -item['price']},
            '$push': {'inventory': item['name']},
            '$set': {f'active_effects.{item["effect"]}': item['effect_value']}
        }
    )
    return True

def get_user_inventory(user_id):
    user = get_user(user_id)
    return user.get('inventory', [])

def get_daily_quests(user_id):
    user = get_user(user_id)
    now = datetime.now()
    
    if user['last_quest_refresh'] is None or (now - user['last_quest_refresh']).days >= 1:
        # Generate new quests
        all_quests = list(quests_collection.find())
        daily_quests = random.sample(all_quests, min(3, len(all_quests)))
        
        users_collection.update_one(
            {'user_id': user_id},
            {
                '$set': {
                    'last_quest_refresh': now,
                    'current_quests': daily_quests
                }
            }
        )
        return daily_quests
    else:
        return user['current_quests']

def complete_quest(user_id, quest_id):
    user = get_user(user_id)
    quest = next((q for q in user['current_quests'] if q['_id'] == quest_id), None)
    
    if quest:
        users_collection.update_one(
            {'user_id': user_id},
            {
                '$pull': {'current_quests': {'_id': quest_id}},
                '$inc': {'balance': quest['reward']}
            }
        )
        return True
    return False

# Add more database operations as needed
