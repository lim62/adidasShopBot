from redis.asyncio import Redis
from aiogram.fsm.storage.redis import RedisStorage
from config import Config, loadConfig

config: Config = loadConfig()

redis = Redis(db=config.redis.db,
              host=config.redis.host,
              port=config.redis.port)
stogare = RedisStorage(redis=redis)