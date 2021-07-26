from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import logging

from .. import elo
from .. import userchoice
from .. import dbworker


def check_none_name(name):
    new_name = ''
    if name is not None:
        new_name = name
    return new_name


class OrderQuestion(StatesGroup):
    """
    Класс состояний конечных автоматов

    """
    waiting_for_answer = State()


class PlayerInfo:
    """
    Информация об игроке

    """

    def __init__(self, name: str):
        self.name = name
        self.rating = None
        self.games = None
        self.new_games = None
        self.new_rating = None

    def set_attributes(self):
        """
        Функция получает из бд текущий рейтинг и количество игр выбранного имени

        """
        parameters = dbworker.dbase.execute_query(f"select rating, games from names.default_names\
                                    where id = md5('{self.name}')::bytea", with_result=True)
        self.rating = int(parameters.rating)
        self.games = int(parameters.games)

    def set_new_attributes(self, old_rating: float, win: int):
        """
        Функция обновляет рейтинг и колиечство игр

        :param old_rating: старый рейтинг
        :param win: кто победил
        """
        self.new_rating = elo.elo(self.rating, old_rating, self.games, win)
        self.new_games = self.games + 1


# Выбор пары
async def winner_become(message: types.Message, state: FSMContext):
    """
    Функция предоставлляет юзеру маркап ответа с именами

    :param message: сообщение
    :param state: состоояние
    """

    user = userchoice.UserChoice(message.from_user.id, check_none_name(message.from_user.first_name) + ' ' +
                                 check_none_name(message.from_user.last_name))
    await state.update_data(chat_user=user)

    user.choose_unrated()

    if user.pair is None:
        await message.reply("Вы оценили все пары! Можете посмотреть общий рейтинг в команде /rating")
        await state.finish()
        return

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    player_one = PlayerInfo(user.players[0])
    player_two = PlayerInfo(user.players[1])

    player_one.set_attributes()
    player_two.set_attributes()

    await state.update_data(player_one=player_one, player_two=player_two)

    keyboard.add(*user.players)

    await message.answer("Кто звучит смешнее?", reply_markup=keyboard)
    await OrderQuestion.waiting_for_answer.set()


async def winner_choose(message: types.Message, state: FSMContext):
    """
    Функция регистриурет ответ пользователя и обновляет данные в бд

    :param message: сообщение
    :param state: состояние
    """
    logging.info(f'Пользователь {message.from_user.first_name} {message.from_user.last_name} сделал выбор')

    user_data = await state.get_data()
    user = user_data['chat_user']

    if message.text not in user.players:
        await message.answer("Пожалуйста, выберите человека, используя клавиатуру ниже.")
        return
    await state.update_data(chosen_name=message.text.lower())
    user_data = await state.get_data()

    win = 1 if user_data['chosen_name'] == user.players[0].lower() else 0
    other = 0 if win == 1 else 1

    player_one = user_data['player_one']
    player_two = user_data['player_two']

    player_one.set_new_attributes(player_two.rating, win)
    player_two.set_new_attributes(player_one.rating, other)

    dbworker.dbase.execute_query(
        query=f"update names.default_names set rating = {player_one.new_rating}, games = {player_one.new_games}\
                    where \"id\" = md5('{player_one.name}')::bytea;\
                update names.default_names set rating = {player_two.new_rating}, games = {player_two.new_games}\
                    where \"id\" = md5('{player_two.name}')::bytea;\
                update names.pairs  set \"users\" = array_append(\"users\", {user.user_id})\
                    where pair = md5('{user.pair}')::bytea")

    await message.reply("Принято! Для оценки следующей пары снова нажмите /rate")
    await state.finish()


def register_handlers_choosing(dp: Dispatcher):
    """
    Регистрация сообщений в диспетчере

    :param dp: диспетчер
    """
    dp.register_message_handler(winner_become, commands="rate", state="*")
    dp.register_message_handler(winner_choose, state=OrderQuestion.waiting_for_answer)
