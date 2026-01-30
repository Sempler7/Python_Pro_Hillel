"""Модуль для витягання IPv4-адрес з тексту"""

import re
from typing import List


def extract_ipv4(text: str) -> List[str]:
    """Витягує всі дійсні IPv4-адреси з наданого тексту."""
    candidate_ips = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', text)

    valid_ips = []
    for ip in candidate_ips:
        parts = ip.split(".")
        if all(0 <= int(part) <= 255 for part in parts):
            valid_ips.append(ip)

    return valid_ips


SOME_TEXT = "Сервери мають адреси 192.168.0.1, 10.0.0.256 і 8.8.8.8."
print(extract_ipv4(SOME_TEXT))  # ['192.168.0.1', '8.8.8.8']
