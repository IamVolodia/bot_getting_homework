from dataclasses import dataclass
from environs import Env

@dataclass
class TgBot:
    token: str
    superadmin_ids: list[int]

@dataclass
class Config:
    tg_bot: TgBot

def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(tg_bot=TgBot(token=env('BOT_TOKEN'), superadmin_ids=map(int, env.list('SUPERADMIN_IDS'))))