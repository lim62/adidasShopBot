from aiogram.filters import BaseFilter
from aiogram.types import Message
from config import Config, loadConfig
from database import getFromTable

config: Config = loadConfig()

class IsAdminFilter(BaseFilter):
    async def __call__(
        self,
        msg: Message = None,
        id: int = None
    ) -> bool:
        toCheck = config.bot.admins
        return (str(msg.from_user.id) in toCheck) or\
            (str(id) in toCheck)
    
class IsModerFilter(BaseFilter):
    async def __call__(
        self,
        msg: Message = None,
        username: str = None
    ) -> bool:
        toCheck = [row[0] for row in getFromTable('moder')]
        return (f'@{msg.from_user.username}' in toCheck) or\
            (username in toCheck)