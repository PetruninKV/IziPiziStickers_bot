from dataclasses import dataclass

from environs import Env


@dataclass
class TgBot:
    token: str
    admin: int


@dataclass
class ObjectsId:
    welcome_stick: str
    processing_stick: str


@dataclass
class Config:
    tg_bot: TgBot
    object_id: ObjectsId


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(token=env('TOKEN'), admin=env.int('ADMIN')),
        object_id=ObjectsId(welcome_stick=env('TOKEN_welcome_stick'),
                            processing_stick=env('TOKEN_processing_stick')),
    )
