"""Автоматичне резервне копіювання"""

import os
import shutil
from typing import Optional, Literal


class BackupContext:
    """
    Менеджер контексту для автоматичного резервного копіювання файлу.
    """

    def __init__(self, original_file: str, temp_file: str):
        self.original_file = original_file
        self.temp_file = temp_file
        self.backup_file: Optional[str] = None

    def __enter__(self) -> str:
        if os.path.exists(self.original_file):
            self.backup_file = self.original_file + ".bak"
            shutil.copy2(self.original_file, self.backup_file)
            print(f"[INFO] Резервна копія створена: {self.backup_file}")
        return self.temp_file

    def __exit__(self, exc_type, exc_val, exc_tb) -> Literal[False]:
        if exc_type is None:
            shutil.move(self.temp_file, self.original_file)
            print(f"[INFO] Оригінал замінено новим: {self.original_file}")
            if self.backup_file and os.path.exists(self.backup_file):
                os.remove(self.backup_file)
                print("[INFO] Резервна копія видалена")
        else:
            if self.backup_file and os.path.exists(self.backup_file):
                shutil.move(self.backup_file, self.original_file)
                print(f"[WARN] Відновлено резервну копію: {self.original_file}")
            if os.path.exists(self.temp_file):
                os.remove(self.temp_file)
                print("[WARN] Тимчасовий файл видалено")
        return False


if __name__ == "__main__":
    with open("important.txt", "w", encoding="utf-8") as f:
        f.write("Старий вміст")

    print("\n--- Успішна обробка ---")
    with BackupContext("important.txt", "important.tmp") as temp:
        with open(temp, "w", encoding="utf-8") as f:
            f.write("Новий вміст без помилок")

    with open("important.txt", "r", encoding="utf-8") as f:
        print("[RESULT] Вміст файлу:", f.read())

    print("\n--- Обробка з помилкою ---")
    try:
        with BackupContext("important.txt", "important.tmp") as temp:
            with open(temp, "w", encoding="utf-8") as f:
                f.write("Новий вміст, але буде помилка")
            raise RuntimeError("Помилка під час обробки")
    except RuntimeError as e:
        print(f"[ERROR] {e}")

    with open("important.txt", "r", encoding="utf-8") as f:
        print("[RESULT] Вміст файлу після помилки:", f.read())
