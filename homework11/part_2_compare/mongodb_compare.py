from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["online_shop"]
products = db["products"]

# CREATE
products.insert_one({"name": "Ноутбук ASUS", "price": 25000, "category": "electronics", "stock": 15})

# READ
for product in products.find():
    print(product)

# UPDATE
products.update_one({"name": "Ноутбук ASUS"}, {"$set": {"stock": 14}})

# DELETE
products.delete_one({"stock": {"$lte": 0}})
