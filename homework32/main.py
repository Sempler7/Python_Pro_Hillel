import asyncio
from aiogram import Bot, Dispatcher
from settings import BOT_TOKEN
from handlers import router


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def main() -> None:
    """Запускає Telegram-бота та ініціалізує маршрути"""

    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())