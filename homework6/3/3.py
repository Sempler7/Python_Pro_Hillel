"""Збір статистики про зображення"""

import os
import csv
from typing import Iterator, Tuple
from PIL import Image


def image_metadata_iterator(directory: str) -> Iterator[Tuple[str, str, Tuple[int, int]]]:
    """Ітератор, що проходить по всіх зображеннях у каталозі та повертає їх метадані"""
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if not os.path.isfile(filepath):
            continue
        try:
            with Image.open(filepath) as img:
                fmt: str = img.format if img.format is not None else "Unknown"
                yield filename, fmt, img.size
        except (OSError, IOError):
            continue


def save_metadata_to_csv(directory: str, output_csv: str) -> None:
    """Зберігає метадані зображень у CSV файл"""
    with open(output_csv, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Filename", "Format", "Width", "Height"])

        for filename, fmt, size in image_metadata_iterator(directory):
            writer.writerow([filename, fmt, size[0], size[1]])


if __name__ == "__main__":
    save_metadata_to_csv("images", "image_metadata.csv")
