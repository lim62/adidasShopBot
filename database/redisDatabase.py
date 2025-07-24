from redis.asyncio import Redis
from aiogram.fsm.storage.redis import RedisStorage

redis = Redis(host='localhost')
stogare = RedisStorage(redis=redis)