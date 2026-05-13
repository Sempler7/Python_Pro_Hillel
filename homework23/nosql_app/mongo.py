from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["django_nosql_db"]
books_collection = db["books"]