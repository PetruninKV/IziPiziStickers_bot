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
class InfluxDB:
    host: str
    org: str
    token: str
    db: str


@dataclass
class FSMMode:
    mode: str


@dataclass
class RedisDB:
    dsn: str
    fsm_db_id: int
    users_db_id: int
    active_users_db_id: int
    blacklist_db_id: int


@dataclass
class Config:
    tg_bot: TgBot
    object_id: ObjectsId
    influxdb: InfluxDB
    fsm_mode: FSMMode
    redis: RedisDB


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(
            token=env('TOKEN'),
            admin=env.int('ADMIN'),
        ),
        object_id=ObjectsId(
            welcome_stick=env('TOKEN_welcome_stick'),
            processing_stick=env('TOKEN_processing_stick'),
        ),
        influxdb=InfluxDB(
            host=env('INFLUXDB_HOST'),
            org=env('INFLUXDB_ORG'),
            token=env('INFLUXDB_TOKEN'),
            db=env('INFLUXDB_DB'),
        ),
        fsm_mode=FSMMode(mode=env('FSM_MODE')),
        redis=RedisDB(
            dsn=env('REDIS__DSN'),
            fsm_db_id=env.int('REDIS__FSM_DB_ID'),
            users_db_id=env.int('REDIS___USERS_DB_ID'),
            active_users_db_id=env.int('REDIS__ACTIVE_USERS_DB_ID'),
            blacklist_db_id=env.int('REDIS__BLACKLIST_DB_ID'),
        ),
    )


config: Config = load_config()
