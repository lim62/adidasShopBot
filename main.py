import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from config import Config, loadConfig
from database import stogare
from middlewares import TheRoleMiddleware
from handlers import (adminRouter,
                      moderRouter,
                      userRouter,
                      otherRouter)

async def main() -> None:
    config: Config = loadConfig()
    logging.basicConfig(level=config.log.level,
                        format=config.log.logFormat,
                        style='{')
    bot = Bot(token=config.bot.TOKEN,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=stogare)
    dp.include_routers(adminRouter, moderRouter, userRouter, otherRouter)
    dp.update.outer_middleware(TheRoleMiddleware())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())