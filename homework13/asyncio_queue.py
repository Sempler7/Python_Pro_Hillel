"""Асинхронні черги"""

import asyncio


async def producer(queue: asyncio.Queue) -> None:
    """Додає 5 завдань до черги з інтервалом у 1 секунду."""
    for i in range(1, 6):
        await asyncio.sleep(1)
        task = f"Завдання {i}"
        await queue.put(task)
        print(f"[Producer] Додано: {task}")


async def consumer(queue: asyncio.Queue, name: str) -> None:
    """Забирає завдання з черги та обробляє його із затримкою у 2 секунди."""
    while True:
        task = await queue.get()
        print(f"[{name}] Отримано: {task}")
        await asyncio.sleep(2)
        print(f"[{name}] Виконано: {task}")
        queue.task_done()


async def main() -> None:
    """Головна функція для запуску producer та consumer."""
    queue: asyncio.Queue[str] = asyncio.Queue()

    producer_task = asyncio.create_task(producer(queue))
    consumers = [
        asyncio.create_task(consumer(queue, f"Consumer-{i}"))
        for i in range(1, 3)
    ]

    await producer_task

    await queue.join()

    for c in consumers:
        c.cancel()


if __name__ == "__main__":
    asyncio.run(main())
