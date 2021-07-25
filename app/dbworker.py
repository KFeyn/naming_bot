from sqlalchemy import create_engine
import pandas as pd
import os


class DbPostgres:
    """
    Класс подключения к БД постгреса

    """

    def __init__(self, login: str, password: str, port: str, db: str, schema: str):
        self.__login = login
        self.__password = password
        self.__port = port
        self.__db = db
        self.__schema = schema

    def execute_query(self, query: str, with_result: bool = False) -> pd.DataFrame:
        """
        Функция подключается к БД постгреса с заданными параметрами используя запрос, если нужно, получает таблицу
        и закрывает подключение. Выводит непустую таблицу, если выполняет select.

        :param query: запрос
        :param with_result: нужно ли выводить таблицу
        :return: вывод таблицы
        """
        engine = create_engine(
            f'postgresql://{self.__login}:{self.__password}@{self.__db}:{self.__port}/{self.__schema}')
        connection = engine.connect()
        query = query.replace('\n', ' ').replace('\t', ' ').replace("'", "\'")
        resoverall = connection.execute(query)
        if with_result:
            table = pd.DataFrame(resoverall.fetchall(), columns=resoverall.keys())
            connection.close()
        else:
            table = pd.DataFrame()
            connection.close()

        return table


dbase = DbPostgres(login=os.environ.get('LOGIN'), password=os.environ.get('PASSWORD'), port=os.environ.get('PORT'),
                   db=os.environ.get('DB'), schema=os.environ.get('SCHEMA'))
