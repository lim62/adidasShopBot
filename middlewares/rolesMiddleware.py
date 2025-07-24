from typing import Any, Callable, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from config import Config, loadConfig
from database import db

config: Config = loadConfig()

class TheRoleMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str: Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str: Any]
    ) -> Any:
        user: User = data['event_from_user']
        if str(user.id) in config.bot.admins:
            data['role'] = 'admin'
        elif f'@{user.username}' in db['moderators']:
            data['role'] = 'moder'
        else:
            data['role'] = 'user'
        return await handler(event, data)