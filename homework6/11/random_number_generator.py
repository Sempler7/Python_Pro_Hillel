"""Генерація txt-файлу із заданою кількістю рядків та випадковими числами"""

import random


def generate_numbers_file(file_path: str, num_lines: int,
                          min_value: int = 0, max_value: int = 100) -> None:
    """Генерує txt-файл з випадковими числами"""
    with open(file_path, "w", encoding="utf-8") as f:
        for _ in range(num_lines):
            number = random.uniform(min_value, max_value)  # випадкове число з плаваючою точкою
            f.write(f"{number:.2f}\n")


generate_numbers_file("data.txt", num_lines=1000, min_value=10, max_value=500)
