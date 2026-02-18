"""Багатопотокове завантаження файлів із мережі."""

import threading
from pathlib import Path
import requests


def download_file(url: str, save_path: Path) -> None:
    """Завантажує файл із мережі та зберігає його локально"""
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()

        with open(save_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)

        print(f"Файл успішно завантажено: {save_path}")
    except requests.RequestException as error:
        print(f"Помилка завантаження {url}: {error}")


def main() -> None:
    """Основна функція для запуску багатопотокового завантаження файлів.
    """
    urls = [
        "https://i.pinimg.com/736x/de/da/fa/dedafa6aa12efb7eff5a3c681c200927.jpg",
        "https://i.pinimg.com/736x/0d/a4/20/0da4201d9b34b1c5c2b2f85930c987ea.jpg",
        "https://i.pinimg.com/736x/fe/cd/9c/fecd9c3f70f2b181f93796cab6f3eed7.jpg",
    ]

    save_dir = Path("downloads")
    save_dir.mkdir(exist_ok=True)

    threads = []
    for url in urls:
        filename = url.rsplit('/', maxsplit=1)[-1]
        save_path = save_dir / filename
        thread = threading.Thread(target=download_file, args=(url, save_path))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("Усі завантаження завершено.")


if __name__ == "__main__":
    main()
