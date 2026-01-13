"""Програма для зчитування великих бінарних файлів блоками.
Автор: Vitalii
"""

from typing import Final

BLOCK_SIZE: Final[int] = 1024


def read_binary_file(file_path: str) -> int:
    """Зчитує бінарний файл великими блоками та повертає кількість прочитаних байтів"""
    total_bytes = 0

    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(BLOCK_SIZE)
            if not chunk:
                break
            total_bytes += len(chunk)

    return total_bytes


if __name__ == "__main__":
    PATHS = ["example.bin", "raw_binary.bin"]

    for path in PATHS:
        bytes_read = read_binary_file(path)
        print(f"Файл: {path} → прочитано {bytes_read} байт")
