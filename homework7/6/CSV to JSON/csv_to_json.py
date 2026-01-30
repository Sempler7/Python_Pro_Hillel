"""Перетворення CSV у JSON"""

import csv
import json


def csv_to_json(csv_file: str, json_file: str) -> None:
    """Перетворює CSV-файл у JSON."""
    with open(csv_file, mode="r", encoding="utf-8") as f_csv:
        reader = csv.DictReader(f_csv)
        data = list(reader)

    with open(json_file, mode="w", encoding="utf-8") as f_json:
        json.dump(data, f_json, ensure_ascii=False, indent=4)


# Використання
csv_to_json("students.csv", "students.json")
