"""Перевірка надійності пароля."""

import re


def check_password(password: str) -> bool:
    """Перевіряє, чи є пароль надійним"""

    if len(password) < 8:
        print("Пароль занадто короткий (мінімум 8 символів).")
        return False

    if not re.search(r"\d", password):
        print("Пароль має містити хоча б одну цифру.")
        return False

    if not re.search(r"[A-Z]", password):
        print("Пароль має містити хоча б одну ВЕЛИКУ літеру.")
        return False

    if not re.search(r"[a-z]", password):
        print("Пароль має містити хоча б одну малу літеру.")
        return False

    if not re.search(r"[@#$%&]", password):
        print("Пароль має містити хоча б один спеціальний символ (@, #, $, %, &).")
        return False

    print("✅ Пароль надійний!")
    return True


check_password("Test123@")
check_password("short1@")
check_password("NoDigits@")
