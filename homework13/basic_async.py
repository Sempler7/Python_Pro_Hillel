"""Асинхронна функція download_page
з обмеженням максимального часу очікування"""

import asyncio
import random


async def download_page(url: str) -> None:
    """Імітація завантаження сторінки з випадковою затримкою."""
    delay = random.randint(1, 10)
    await asyncio.sleep(delay)
    print(f"Сторінка {url} завантажена за {delay} секунд.")


async def main(urls: list[str]) -> None:
    """Головна функція для завантаження сторінок з обмеженням часу очікування."""
    tasks = []
    for url in urls:
        task = asyncio.wait_for(download_page(url), timeout=5)
        tasks.append(task)

    for url, task in zip(urls, tasks):
        try:
            await task
        except asyncio.TimeoutError:
            print(f"Таймаут: {url} не відповів за 5 секунд.")


if __name__ == "__main__":
    list_urls = [
        "https://ukr.net",
        "https://python.org",
        "https://rozetka.com.ua",
        "https://github.com"
    ]

    asyncio.run(main(list_urls))
