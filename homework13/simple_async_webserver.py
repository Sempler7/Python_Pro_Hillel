"""Простий асинхронний веб-сервер на базі aiohttp."""

import asyncio
from aiohttp import web


async def handle_root(request: web.Request) -> web.Response:  # pylint: disable=unused-argument
    """Обробник для маршруту '/'."""
    return web.Response(text="Hello, World!")


async def handle_slow(request: web.Request) -> web.Response:  # pylint: disable=unused-argument
    """Обробник для маршруту '/slow' з симуляцією довгої операції."""
    await asyncio.sleep(5)
    return web.Response(text="Operation completed")


def main() -> None:
    """Запуск асинхронного веб-сервера."""
    app = web.Application()
    app.router.add_get("/", handle_root)
    app.router.add_get("/slow", handle_slow)

    web.run_app(app, host="127.0.0.1", port=8080)


if __name__ == "__main__":
    main()
