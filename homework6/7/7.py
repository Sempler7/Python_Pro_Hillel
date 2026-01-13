"""Парсинг великих лог-файлів для аналітики"""

from typing import Generator


def error_lines_generator(log_file_path: str) -> Generator[str, None, None]:
    """Генератор для построкового читання великого лог-файлу
    та повернення лише рядків з кодами помилок (4XX, 5XX)"""
    with open(log_file_path, "r", encoding="utf-8") as file:
        for line in file:
            parts = line.split()
            if len(parts) > 8:
                try:
                    status_code = int(parts[8])
                    if 400 <= status_code < 600:
                        yield line.strip()
                except ValueError:
                    continue


def save_errors(log_file_path: str, output_file_path: str) -> None:
    """Зберігає всі рядки з помилками у окремий файл"""
    with open(output_file_path, "w", encoding="utf-8") as out_file:
        for error_line in error_lines_generator(log_file_path):
            out_file.write(error_line + "\n")


if __name__ == "__main__":
    INPUT_LOG = "big_log.log"
    OUTPUT_LOG = "errors.log"
    save_errors(INPUT_LOG, OUTPUT_LOG)
    print(f"Помилки збережено у файл: {OUTPUT_LOG}")
