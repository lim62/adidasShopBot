from dataclasses import dataclass
from environs import Env

@dataclass
class LoggingConfig:
    level: str
    logFormat: str

@dataclass
class TgBot:
    TOKEN: str
    admins: list[str]

@dataclass
class DatabaseConfig:
    name: str
    host: str
    port: int
    user: str
    password: str

@dataclass
class RedisConfig:
    host: str

@dataclass
class Config:
    bot: TgBot
    db: DatabaseConfig
    redis: RedisConfig
    log: LoggingConfig

def loadConfig(path: str | None = None) -> Config:
    env: Env = Env()
    env.read_env(path, override=True)
    return Config(
        bot=TgBot(
            TOKEN=env('TOKEN'),
            admins=env('ADMINS_IDS')
        ),
        db=DatabaseConfig(
            name=env("POSTGRES_DB"),
            host=env("POSTGRES_HOST"),
            port=env.int("POSTGRES_PORT"),
            user=env("POSTGRES_USER"),
            password=env("POSTGRES_PASSWORD")
        ),
        redis=RedisConfig(
            host=env('REDIS_HOST')
        ),
        log=LoggingConfig(
            level=env('loggingLevel'),
            logFormat=env('loggingFormat')
        )
    )