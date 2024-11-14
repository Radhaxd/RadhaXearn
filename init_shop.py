
from pymongo import MongoClient
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client['refer_earn_bot']
shop_items_collection = db['shop_items']

initial_items = [
    {
        "name": "VIP Status",
        "description": "Get VIP status and exclusive perks!",
        "price": 100
    },
    {
        "name": "XP Booster",
        "description": "Double your XP gain for 24 hours!",
        "price": 50
    },
    {
        "name": "Lucky Charm",
        "description": "Increase your chances of winning in mini-games!",
        "price": 75
    },
    {
        "name": "Mystery Box",
        "description": "Contains a random reward!",
        "price": 25
    }
]

def init_shop():
    shop_items_collection.delete_many({})  # Clear existing items
    shop_items_collection.insert_many(initial_items)
    print(f"{len(initial_items)} items added to the shop.")

if __name__ == "__main__":
    init_shop()
