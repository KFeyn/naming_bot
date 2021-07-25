import psycopg2
import pandas as pd
import os


class DbPostgres:
    """
    Класс подключения к БД постгреса

    """

    def __init__(self, db_url: str):
        self.__db_url = db_url

    def execute_query(self, query: str, with_result: bool = False) -> pd.DataFrame:
        """
        Функция подключается к БД постгреса с заданными параметрами используя запрос, если нужно, получает таблицу
        и закрывает подключение. Выводит непустую таблицу, если выполняет select.

        :param query: запрос
        :param with_result: нужно ли выводить таблицу
        :return: вывод таблицы
        """
        connection = psycopg2.connect(self.__db_url, sslmode='require')
        query = query.replace('\n', ' ').replace('\t', ' ').replace("'", "\'")

        if with_result:
            table = pd.io.sql.read_sql_query(query, connection)
            connection.close()
        else:
            cur = connection.cursor()
            cur.execute(query)
            table = pd.DataFrame()
            cur.close()
            connection.commit()
            connection.close()

        return table


dbase = DbPostgres(os.environ.get('DATABASE_URL'))
