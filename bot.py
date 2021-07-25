import asyncio
import logging
import os

from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher

from app.handlers.rate import register_handlers_choosing
from app.handlers.common import register_handlers_common
from app.handlers.rating import register_handlers_rating
from app.handlers.addnames import register_handlers_add_names

logger = logging.getLogger(__name__)


async def set_commands(bot: Bot):
    """
    Функция регистрирует команды для бота

    :param bot: бот
    """
    commands = [
        BotCommand(command="/rate", description="Выбрать из пары"),
        BotCommand(command="/rating", description="Общий рейтинг"),
        BotCommand(command="/help", description="Помощь")
    ]
    await bot.set_my_commands(commands)


async def main():
    """
    Основная функция, запускающая бота

    """

    # Настройка логирования в stdout
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    bot = Bot(token=os.environ['TOKEN'])
    dp = Dispatcher(bot, storage=MemoryStorage())

    # Регистрация хэндлеров
    register_handlers_choosing(dp)
    register_handlers_common(dp)
    register_handlers_rating(dp)
    register_handlers_add_names(dp)

    # Установка команд бота
    await set_commands(bot)

    # Запуск поллинга
    # await dp.skip_updates()  # пропуск накопившихся апдейтов (необязательно)
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
