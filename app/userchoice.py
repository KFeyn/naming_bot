import random
import dbworker


class UserChoice:
    """
    Класс выбора пользователя - помимо инфы о пользователе запминает того, кто выбран для оценки

    """

    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.pair = None
        self.players = None

    def check_name(self):
        """
        Функция проверяет, есть ли данный пользователь в бд

        """
        if not dbworker.dbase.execute_query(query=f"select telegram_id from names.users\
                    where telegram_id = {self.user_id}", with_result=True).telegram_id.any():
            dbworker.dbase.execute_query(f"insert into names.users values ({self.user_id}, '{self.name}')")

    def choose_unrated(self):
        """
        Функция ищет неоценные пары в бд и выдает произвольную пару

        """
        unrated = list(dbworker.dbase.execute_query(query=f"select fio_pair from names.pairs\
                    where not ({self.user_id} = any(users ))", with_result=True).fio_pair)
        if not unrated:
            self.pair = None
            self.players = None
        else:
            self.pair = random.choice(unrated)
            self.players = self.pair.split('-')
