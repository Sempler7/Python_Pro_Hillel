"""Скрипт для завантаження вебсторінки та збереження її у файл"""

import requests


def download_page(url: str, filename: str = "site_info.txt") -> None:
    """Завантажує сторінку за вказаним URL та зберігає її вміст у текстовий файл"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        with open(filename, "w", encoding="utf-8") as file:
            file.write(response.text)
        print(f"Сторінку успішно збережено у файл: {filename}")
    except requests.exceptions.RequestException as e:
        print(f"Помилка при завантаженні сторінки: {e}")


if __name__ == "__main__":
    SITE = "https://ithillel.ua/"
    download_page(SITE)
