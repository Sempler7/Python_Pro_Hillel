"""Архівування та зберігання великих даних"""

import zipfile
from pathlib import Path
from typing import List


class ArchiveManager:
    """
    Менеджер контексту для архівування файлів у ZIP.
    Використання:
        with ArchiveManager("backup.zip", ["file1.txt", "file2.txt"]) as arc:
            pass  # архівування відбувається автоматично
    """

    def __init__(self, archive_name: str, files: List[str]) -> None:
        self.archive_name = archive_name
        self.files = files
        self.zip_file: zipfile.ZipFile | None = None

    def __enter__(self) -> zipfile.ZipFile:
        # Створюємо архів у режимі запису
        self.zip_file = zipfile.ZipFile(
            self.archive_name, mode="w",
            compression=zipfile.ZIP_DEFLATED)
        for file in self.files:
            path = Path(file)
            if path.exists():
                self.zip_file.write(path, arcname=path.name)
            else:
                print(f"⚠️ Файл {file} не знайдено, пропускаю.")
        return self.zip_file

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        # Закриваємо архів
        if self.zip_file:
            self.zip_file.close()
        print(f"✅ Архів '{self.archive_name}' створено та закрито.")


files_to_archive = ["data1.csv", "HELLO.pdf", "dudububu.jpg"]

with ArchiveManager("my_archive.zip", files_to_archive):
    print("Файли архівуються...")
