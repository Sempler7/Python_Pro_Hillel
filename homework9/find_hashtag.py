"""Модуль для пошуку хеш-тегів в тексті"""

import re
from typing import List


def extract_hashtags(text: str) -> List[str]:
    """Повертає список хеш-тегів з тексту"""
    pattern = r"#([A-Za-zА-Яа-яІіЇїЄєҐґ0-9]+)"
    return re.findall(pattern, text)


SAMPLE_TEXT = "Сьогодні гарний день! #sunshine #2026 #ПривітСвіт #hello_world"
hashtags = extract_hashtags(SAMPLE_TEXT)

print(hashtags)  # ['sunshine', '2026', 'ПривітСвіт']
