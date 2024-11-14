
from pymongo import MongoClient
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client['refer_earn_bot']
users_collection = db['users']

def get_user(user_id):
    return users_collection.find_one({'user_id': user_id})

def create_user(user_id):
    user = {
        'user_id': user_id,
        'balance': 0,
        'referrals': [],
        'joined_date': datetime.now()
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

# Add more database operations as needed
