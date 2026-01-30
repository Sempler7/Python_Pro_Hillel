"""Аналіз логів вебсервера:
підрахунок кількості запитів з різних IP-адрес.
"""

from collections import Counter
from typing import Dict


def parse_log_file(file_path: str) -> Dict[str, int]:
    """Читає лог-файл та повертає словник з кількістю запитів для кожного IP"""
    ip_counter: Counter[str] = Counter()

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.split()
            if parts:
                ip = parts[0]
                ip_counter[ip] += 1

    return dict(ip_counter)


def print_statistics(stats: Dict[str, int]) -> None:
    """Виводить статистику у зручному форматі"""
    print("Статистика запитів за IP-адресами:")
    print("-" * 40)
    for ip, count in sorted(stats.items(), key=lambda x: x[1], reverse=True):
        print(f"{ip:20} -> {count} запитів")


if __name__ == "__main__":
    LOG_FILE = "access.log"
    all_stats = parse_log_file(LOG_FILE)
    print_statistics(all_stats)
