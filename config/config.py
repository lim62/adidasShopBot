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
class Config:
    bot: TgBot
    log: LoggingConfig

def loadConfig(path: str | None = None) -> Config:
    env: Env = Env()
    env.read_env(path, override=True)
    return Config(
        bot=TgBot(
            TOKEN=env('TOKEN'),
            admins=env('admins')
        ),
        log=LoggingConfig(
            level=env('loggingLevel'),
            logFormat=env('loggingFormat')
        )
    )