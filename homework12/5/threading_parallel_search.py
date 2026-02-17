"""Паралельний пошук тексту у файлах за допомогою threading"""

import threading
from typing import List


def search_in_file(filename: str, text: str) -> None:
    """Шукає текст у файлі та виводить рядки з результатами."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            for i, line in enumerate(file, start=1):
                if text in line:
                    print(f"[{filename}] рядок {i}: {line.strip()}")
    except FileNotFoundError:
        print(f"Файл {filename} не знайдено.")
    except OSError as err:
        print(f"Помилка при читанні {filename}: {err}")


def parallel_search(file_list: List[str], text: str) -> None:
    """Запускає паралельний пошук у кількох файлах."""
    threads: List[threading.Thread] = []
    for fname in file_list:
        thread = threading.Thread(target=search_in_file, args=(fname, text))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    files = ["file1.txt", "file2.txt"]
    parallel_search(files, "мільйони")
