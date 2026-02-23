"""Порівняння продуктивності різних підходів до виконання HTTP-запитів."""

import time
import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

import requests
import aiohttp
from tabulate import tabulate  # type: ignore[import-untyped]

URL = "https://httpbin.org/get"


def sync_requests(n=500):
    """Синхронний метод для виконання n HTTP-запитів."""
    start = time.perf_counter()
    for _ in range(n):
        try:
            requests.get(URL, timeout=5)
        except requests.exceptions.RequestException as e:
            print(f"Sync error: {e}")
    return time.perf_counter() - start


def safe_request_thread(_):
    """Безпечний метод для виконання HTTP-запиту в потоці."""
    try:
        requests.get(URL, timeout=5)
    except requests.exceptions.RequestException as e:
        print(f"Thread error: {e}")


def thread_requests(n=500):
    """Багатопотоковий метод для виконання n HTTP-запитів."""
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=50) as executor:
        list(executor.map(safe_request_thread, range(n)))
    return time.perf_counter() - start


def safe_request_process(_):
    """Безпечний метод для виконання HTTP-запиту в процесі."""
    try:
        requests.get(URL, timeout=5)
    except requests.exceptions.RequestException as e:
        print(f"Process error: {e}")


def process_requests(n=500):
    """Багатопроцесорний метод для виконання n HTTP-запитів."""
    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=8) as executor:
        list(executor.map(safe_request_process, range(n)))
    return time.perf_counter() - start


async def fetch(session):
    """Асинхронний метод для виконання одного HTTP-запиту."""
    try:
        async with session.get(URL) as resp:
            await resp.text()
    except aiohttp.ClientError as e:
        print(f"Async error: {e}")


async def async_requests(n=500):
    """Асинхронний метод для виконання n HTTP-запитів."""
    start = time.perf_counter()
    timeout = aiohttp.ClientTimeout(total=5)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        tasks = [fetch(session) for _ in range(n)]
        await asyncio.gather(*tasks, return_exceptions=True)
    return time.perf_counter() - start


if __name__ == "__main__":
    results = [("Синхронний", sync_requests()),
               ("Багатопотоковий", thread_requests()),
               ("Багатопроцесорний", process_requests()),
               ("Асинхронний", asyncio.run(async_requests()))]

    print(tabulate(results, headers=["Режим", "Час (сек)"], tablefmt="github"))


""" Результат:

| Режим             |   Час (сек) |
|-------------------|-------------|
| Синхронний        |   520.45    |
| Багатопотоковий   |    49.3545  |
| Багатопроцесорний |    69.1133  |
| Асинхронний       |     3.23876 |

"""
