"""Модуль для вилучення URL-адрес з тексту"""

import re
from typing import List


def extract_urls(text: str) -> List[str]:
    """Вилучає всі URL-адреси з заданого тексту"""
    url_pattern = re.compile(
        r'(https?://[^\s]+|ftp://[^\s]+|www\.[^\s]+)',
        re.IGNORECASE
    )
    return url_pattern.findall(text)


if __name__ == "__main__":
    SAMPLE_TEXT = (
        "Ось кілька посилань: https://example.com, "
        "ftp://files.server.net, а також www.test.org"
        "та http://another-example.com/page.html"
    )
    urls = extract_urls(SAMPLE_TEXT)
    print("Знайдені URL:", urls)
