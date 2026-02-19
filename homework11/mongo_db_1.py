"""Приклад роботи з MongoDB для онлайн-магазину."""

from datetime import datetime, timedelta
from pymongo import MongoClient  # type: ignore[import-untyped]

# Підключення
client = MongoClient("mongodb://localhost:27017/")
db = client["online_shop"]

products = db["products"]
orders = db["orders"]

# CREATE
products.insert_many([
    {"name": "Ноутбук ASUS", "price": 25000, "category": "electronics", "stock": 15},
    {"name": "Смартфон Samsung", "price": 18000, "category": "electronics", "stock": 30},
    {"name": "Книга 'Python Basics'", "price": 500, "category": "books", "stock": 50}
])

orders.insert_one({
    "order_id": 1001,
    "customer": "Іван Петренко",
    "products": [
        {"product_id": 1, "quantity": 1},
        {"product_id": 3, "quantity": 2}
    ],
    "total": 26000,
    "date": datetime.now()
})

# READ (замовлення за останні 30 днів)
last_30_days = datetime.now() - timedelta(days=30)
recent_orders = orders.find({"date": {"$gte": last_30_days}})
for order in recent_orders:
    print(order)

# UPDATE (оновлення кількості на складі)
products.update_one({"name": "Ноутбук ASUS"}, {"$inc": {"stock": -1}})

# DELETE (видалення недоступних продуктів)
products.delete_many({"stock": {"$lte": 0}})

# AGGREGATION (кількість проданих продуктів)
pipeline = [
    {"$unwind": "$products"},
    {"$group": {"_id": "$products.product_id", "totalSold": {"$sum": "$products.quantity"}}}
]
for result in orders.aggregate(pipeline):
    print(result)

products.create_index("category")
