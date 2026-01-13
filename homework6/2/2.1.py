"""Ітератор для генерації унікальних ідентифікаторів на основі генерації хешів"""

import hashlib
import time
from typing import Iterator


class HashIDIterator:
    """
    Ітератор для генерації унікальних ідентифікаторів
    на основі SHA256 від часу та лічильника.
    """

    def __init__(self) -> None:
        self.counter = 0

    def __iter__(self) -> Iterator[str]:
        return self

    def __next__(self) -> str:
        self.counter += 1
        raw = f"{time.time_ns()}-{self.counter}"
        return hashlib.sha256(raw.encode()).hexdigest()


if __name__ == "__main__":
    iterator = HashIDIterator()
    for _ in range(5):
        print(next(iterator))
