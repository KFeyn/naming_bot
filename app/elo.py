def elo(guy1: float, guy2: float, games1: int, winner: int) -> float:
    """
    Функция для подсчета рейтингов при помощи рейтинга Эло.

    :param guy1: текущий рейтинг первого
    :param guy2: текущий рейтинг вторго
    :param games1: количество игр первого
    :param winner: победитель
    :return: возвращает обновленный рейтинг первого игрока
    """
    k = 40 if games1 <= 30 else 20 if guy1 < 2400 else 10
    points = 1 / (1 + 10 ** ((guy2 - guy1) / 400))
    new_rating = guy1 + k * (winner - points)

    return new_rating
