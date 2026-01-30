"""Перетворення JSON у CSV"""

import csv
import json


def json_to_csv(json_file: str, csv_file: str) -> None:
    """Перетворює JSON-файл у CSV."""
    with open(json_file, mode="r", encoding="utf-8") as f_json:
        data = json.load(f_json)

    # Визначаємо заголовки з ключів першого елемента
    headers = data[0].keys()

    with open(csv_file, mode="w", encoding="utf-8", newline="") as f_csv:
        writer = csv.DictWriter(f_csv, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)


# Використання
json_to_csv("books.json", "JSON to CSV/books.csv")
