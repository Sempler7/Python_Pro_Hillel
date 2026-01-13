"""Конфігурація через контекстні менеджери"""

import json
import configparser
from pathlib import Path
from typing import Union


class ConfigManager:
    """
    Контекстний менеджер для роботи з конфігураційними файлами (.json або .ini).
    Автоматично читає дані при вході та зберігає зміни при виході.
    """

    def __init__(self, file_path: Union[str, Path]):
        self.file_path = Path(file_path)
        self.config = None
        self.format = None

    def __enter__(self):
        if self.file_path.suffix == ".json":
            self.format = "json"
            if self.file_path.exists():
                with open(self.file_path, "r", encoding="utf-8") as f:
                    self.config = json.load(f)
            else:
                self.config = {}
        elif self.file_path.suffix == ".ini":
            self.format = "ini"
            self.config = configparser.ConfigParser()
            if self.file_path.exists():
                self.config.read(self.file_path, encoding="utf-8")
        else:
            raise ValueError("Підтримуються лише формати .json та .ini")

        return self.config

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.format == "json":
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        elif self.format == "ini":
            with open(self.file_path, "w", encoding="utf-8") as f:
                self.config.write(f)
        # Якщо сталася помилка — не приглушуємо її
        return False


# === Приклад використання ===

# JSON
with ConfigManager("config.json") as cfg:
    cfg["debug"] = True
    cfg["db_host"] = "localhost"

# INI
with ConfigManager("config.ini") as cfg:
    if "server" not in cfg:
        cfg["server"] = {}
    cfg["server"]["host"] = "127.0.0.1"
    cfg["server"]["port"] = "8080"
