"""Асинхронний таймаут"""

import asyncio


async def slow_task():
    """Імітує довге завдання (10 секунд)."""
    print("Початок виконання slow_task()...")
    await asyncio.sleep(10)
    print("Завдання завершено!")


async def main():
    """Головна функція для запуску завдання з таймаутом."""
    try:
        await asyncio.wait_for(slow_task(), timeout=5)
    except asyncio.TimeoutError:
        print("⏱ Перевищено час очікування (5 секунд).")


asyncio.run(main())
