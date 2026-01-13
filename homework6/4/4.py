"""Генератор для обробки великих файлів"""

from typing import Generator


def keyword_filter(file_path: str, keyword: str) -> Generator[str, None, None]:
    """Генератор для построкового читання великого файлу.
    Повертає лише ті рядки, що містять задане ключове слово
    """
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            if keyword in line:
                yield line.rstrip("\n")


def filter_and_save(input_file: str, output_file: str, keyword: str) -> None:
    """Використовує генератор для фільтрації рядків та записує їх у новий файл"""
    with open(output_file, "w", encoding="utf-8") as out_file:
        for line in keyword_filter(input_file, keyword):
            out_file.write(line + "\n")


if __name__ == "__main__":
    INPUT_PATH = "big_log.txt"
    OUTPUT_PATH = "filtered_log.txt"
    SEARCH_WORD = "ERROR"

    filter_and_save(INPUT_PATH, OUTPUT_PATH, SEARCH_WORD)
    print(f"Відфільтровані рядки збережено у {OUTPUT_PATH}")
