"""Завантаження зображень з декількох сайтів"""

import os
import asyncio
import aiohttp  # type: ignore[import-untyped]
import aiofiles  # type: ignore[import-untyped]


async def download_image(url: str, filename: str, folder: str = "images") -> None:
    """Завантажує зображення за вказаним URL та зберігає його у файл у папці folder"""
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                async with aiofiles.open(filepath, mode='wb') as f:
                    await f.write(await response.read())
                print(f"Зображення збережено: {filepath}")
            else:
                print(f"Помилка {response.status} при завантаженні {url}")


async def main():
    """Головна функція для завантаження зображень."""
    images = [
        ("https://ict.uu.edu.ua/vykladachi/mzokov-volodymyr-hennadijovych/", "mzokov.jpg"),
        ("https://seoport.com.ua/2023/08/15/sunstitch-in-ua/", "1692101579161-750x365.jpg"),
        ("https://www.education.ua/articles/956/", "956b.png"),
    ]

    tasks = [download_image(url, filename) for url, filename in images]

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
