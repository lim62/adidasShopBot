from aiogram.filters import BaseFilter
from aiogram.types import Message
from config import Config, loadConfig
from database import db

config: Config = loadConfig()

class IsAdminFilter(BaseFilter):
    async def __call__(
        self,
        msg: Message = None,
        id: int = None
    ) -> bool:
        return (str(msg.from_user.id) in config.bot.admins) or\
            (str(id) in config.bot.admins)
    
class IsModerFilter(BaseFilter):
    async def __call__(
        self,
        msg: Message = None,
        username: str = None
    ) -> bool:
        return (f'@{msg.from_user.username}' in db['moderators']) or\
            (username in db['moderators'])