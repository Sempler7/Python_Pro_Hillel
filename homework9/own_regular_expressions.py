"""Власні регулярні вирази"""

import re

# Пошук певних слів у тексті
pattern_python = re.compile(r"(?i)\bpython\b")
TEXT = "Я люблю Python і pythonic стиль."
print(pattern_python.findall(TEXT))

# Перевірка формату даних
pattern_email = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
print(bool(pattern_email.match("test@example.com")))

pattern_phone = re.compile(r"^\+380\d{9}$")
print(bool(pattern_phone.match("+380931234567")))

pattern_postcode = re.compile(r"^\d{5}$")
print(bool(pattern_postcode.match("01001")))

# Дата у форматі DD.MM.YYYY
pattern_date = re.compile(r"^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.\d{4}$")
print(bool(pattern_date.match("30.01.2026")))

# Знайти всі слова, що починаються з великої літери
pattern_capitalized = re.compile(r"\b[A-ZА-ЯЇЄІ][a-zа-яїєі]*\b")
TEXT2 = "Kyiv є столицею України."
print(pattern_capitalized.findall(TEXT2))

# Знайти всі числа у тексті
pattern_numbers = re.compile(r"\d+")
TEXT3 = "У мене є 3 яблука і 25 груш."
print(pattern_numbers.findall(TEXT3))
