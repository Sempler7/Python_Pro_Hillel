"""Генератор для створення нескінченної послідовності"""

from typing import Generator, Optional, TextIO


def even_numbers() -> Generator[int, None, None]:
    """Генератор нескінченної послідовності парних чисел."""
    n = 0
    while True:
        yield n
        n += 2


class LimitAndSave:
    """Менеджер контексту для обмеження кількості чисел та збереження у файл."""

    def __init__(self, filename: str, limit: int = 100) -> None:
        """Ініціалізація менеджера контексту"""
        self.filename: str = filename
        self.limit: int = limit
        self.file: Optional[TextIO] = None

    def __enter__(self):
        """Відкриття файлу для запису"""
        self.file = open(self.filename, "w", encoding="utf-8")
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Закриття файлу"""
        if self.file:
            self.file.close()


if __name__ == "__main__":
    gen = even_numbers()
    with LimitAndSave("even_numbers.txt", limit=100) as f:
        for i, num in enumerate(gen):
            if i >= 100:
                break
            f.write(f"{num}\n")
