"""Ітератор для генерації унікальних ідентифікаторів на основі uuid4"""

import uuid
from typing import Iterator


class UniqueIDIterator:
    """
    Ітератор для генерації унікальних ідентифікаторів.

    Використовує UUID4 для створення випадкових, гарантовано унікальних
    ідентифікаторів при кожній ітерації.
    """

    def __iter__(self) -> Iterator[str]:
        """Повертає сам ітератор"""
        return self

    def __next__(self) -> str:
        """Генерує та повертає наступний унікальний ідентифікатор"""
        return str(uuid.uuid4())


if __name__ == "__main__":
    iterator = UniqueIDIterator()
    for _ in range(5):
        print(next(iterator))
