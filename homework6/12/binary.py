"""Створення бінарного файлу з «сирими» байтами"""

import os

with open("raw_binary.bin", "wb") as f:
    f.write(os.urandom(64))  # 64 випадкових байти
