"""Модуль для пошуку телефонних номерів у тексті."""

import re
from typing import List


def find_phone_numbers(text: str) -> List[str]:
    """Пошук телефонних номерів у тексті"""
    pattern = re.compile(
        r"""
        (?:\(\d{3}\)\s?\d{3}[-.]\d{4})   # (123) 456-7890
        |(?:\d{3}[-.]\d{3}[-.]\d{4})     # 123-456-7890 або 123.456.7890
        |(?:\d{10})                      # 1234567890
        """, re.VERBOSE
    )
    return pattern.findall(text)


if __name__ == "__main__":
    SAMPLE_TEXT = """
    Мої номери: (123) 456-7890, 123-456-7890,
    ще один: 123.456.7890 і простий 1234567890.
    """
    print(find_phone_numbers(SAMPLE_TEXT))
