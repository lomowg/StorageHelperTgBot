from dataclasses import dataclass

from environs import Env


@dataclass
class UserDB:
    user: str
    password: str


@dataclass
class DB:
    host: str
    port: int
    db_name: str


@dataclass
class ConnectionsPool:
    db: DB
    user: UserDB


@dataclass
class TgBot:
    token: str
    encrypt_key: bytes


@dataclass
class Config:
    tg_bot: TgBot
    con_pool: ConnectionsPool


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN'), encrypt_key=env('ENCRYPT_KEY')),
                  con_pool=ConnectionsPool(db=DB(host=env('HOST'),
                                                 port=int(env('PORT')),
                                                 db_name=env('DATABASE')),
                                           user=UserDB(user=env('USER'),
                                                       password=env('PASSWORD'))))
