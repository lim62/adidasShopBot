from redis.asyncio import Redis
from aiogram.fsm.storage.redis import RedisStorage
from config import Config, loadConfig

config: Config = loadConfig()

redis = Redis(host=config.redis.host)
stogare = RedisStorage(redis=redis)