import configparser
from dataclasses import dataclass


@dataclass
class TgBot:
    token: str


@dataclass
class DataBase:
    login: str
    password: str
    port: str
    db: str
    schema: str


@dataclass
class Config:
    tg_bot: TgBot
    d_b: DataBase


def load_config(path: str) -> Config:
    """
    Загрузка конфига

    :param path: путь в основной папке, где лежит конфиг
    :return: выводит конфиг
    """
    config = configparser.ConfigParser()
    config.read(path)

    tg_bot = config["tg_bot"]
    d_b = config["d_b"]

    return Config(
        tg_bot=TgBot(token=tg_bot["token"]),
        d_b=DataBase(login=d_b["login"], password=d_b["password"], port=d_b["port"], db=d_b["db"], schema=d_b["schema"])
    )
