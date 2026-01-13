"""Інкрементне обчислення середніх значень (опціонально)"""

from typing import Generator


def incremental_mean(file_path: str) -> Generator[float, None, None]:
    """Генератор для інкрементного обчислення середнього значення"""
    total = 0.0
    count = 0

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                value = float(line.strip())
            except ValueError:
                continue

            count += 1
            total += value
            yield total / count


for avg in incremental_mean("data.txt"):
    print(f"Поточне середнє: {avg:.2f}")
