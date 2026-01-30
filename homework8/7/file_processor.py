"""Тестування з використанням фікстур та тимчасових файлів"""

import os


class FileProcessor:
    """`"""

    @staticmethod
    def write_to_file(file_path: str, data: str) -> None:
        """Записує дані у файл."""
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(data)

    @staticmethod
    def read_from_file(file_path: str) -> str:
        """Читає дані з файлу. Якщо файл не існує — піднімає FileNotFoundError."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл {file_path} не знайдено")
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
