"""Ітерація через файли в каталозі"""

import os
from typing import Iterator, Tuple


def file_iterator(directory: str) -> Iterator[Tuple[str, int]]:
    """Ітератор для проходження по файлах у заданому каталозі"""
    with os.scandir(directory) as entries:
        for entry in entries:
            if entry.is_file():
                yield entry.name, entry.stat().st_size


if __name__ == "__main__":
    PATH = "."
    for filename, size in file_iterator(PATH):
        print(f"{filename} — {size} байт")
