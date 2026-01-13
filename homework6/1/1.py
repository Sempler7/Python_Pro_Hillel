"""Створення власного ітератора для зворотного читання файлу"""

from typing import Iterator


class ReverseFileIterator:
    """
    Ітератор для зчитування файлу у зворотному порядку (рядок за рядком)"""

    def __init__(self, filename: str) -> None:
        """Ініціалізує ітератор, зчитує всі рядки у пам'ять"""
        self.filename = filename
        with open(filename, "r", encoding="utf-8") as f:
            self.lines = f.readlines()
        self.index = len(self.lines) - 1

    def __iter__(self) -> Iterator[str]:
        """Повертає сам ітератор"""
        return self

    def __next__(self) -> str:
        """Повертає наступний рядок файлу у зворотному порядку"""
        if self.index < 0:
            raise StopIteration
        line = self.lines[self.index].rstrip("\n")
        self.index -= 1
        return line


iterator = ReverseFileIterator("log.txt")

for row in iterator:
    print(row)
