"""Модуль для видалення HTML-тегів з тексту"""

import re


def remove_html_tags(text: str) -> str:
    """Видаляє всі HTML-теги з тексту"""
    clean = re.sub(r'<.*?>', '', text)
    return clean


# Приклад використання
HTML_TEXT = "<p>Привіт, <b>світ</b>!</p>"
print(remove_html_tags(HTML_TEXT))  # Виведе: Привіт, світ!
