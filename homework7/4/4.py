import json
from pprint import pprint

with open("books.json", "r", encoding="utf-8") as file:
    books = json.load(file)

print("📚 Доступні книги:")
for book in books:
    if book["наявність"]:
        print(f"- {book['назва']} ({book['автор']}, {book['рік']})")

new_book = {
    "назва": "Амбер",
    "автор": "А.Азімов",
    "рік": 1981,
    "наявність": True
}

books.append(new_book)

with open("books.json", "w", encoding="utf-8") as file:
    json.dump(books, file, ensure_ascii=False, indent=2)

print("\nНова книга додана і файл оновлено.")

print("📚 Доступні книги:")
for book in books:
    if book["наявність"]:
        print(f"- {book['назва']} ({book['автор']}, {book['рік']})")
