"""Завдання: Використання асинхронних HTTP-запитів"""

import asyncio
import aiohttp
from aiohttp import ClientError


async def fetch_content(url: str) -> str:
    """Виконує HTTP-запит до вказаного URL та повертає вміст сторінки"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.text()
                return f"Помилка: отримано статус {response.status} для {url}"
    except ClientError as e:
        return f"Помилка підключення до {url}: {e}"
    except asyncio.TimeoutError:
        return f"Помилка: таймаут при зверненні до {url}"


async def fetch_all(urls: list[str]) -> list[str]:
    """Приймає список URL і завантажує вміст усіх сторінок паралельно"""
    tasks = [fetch_content(url) for url in urls]
    results = await asyncio.gather(*tasks)
    return list(results)


if __name__ == "__main__":
    some_urls = [
        "https://www.python.org",
        "https://docs.aiohttp.org",
        "https://nonexistent.example.com"
    ]

    contents = asyncio.run(fetch_all(some_urls))
    for i, content in enumerate(contents, start=1):
        print(f"--- Результат {i} ---")
        print(content[:200], "...")
