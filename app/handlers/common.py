import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
import aiogram.utils.markdown as fmt

from .. import userchoice


def check_none_name(name):
    new_name = ''
    if name is not None:
        new_name = name
    return new_name


async def starting_message(message: types.Message, state: FSMContext):
    """
    Первая команда, она проверяет существование пользователя и заполняет его данные

    :param message: сообщение
    :param state: состояние
    """
    await state.finish()

    first_name = check_none_name(message.from_user.first_name)
    last_name = check_none_name(message.from_user.last_name)

    user = userchoice.UserChoice(message.from_user.id, first_name + ' ' + last_name)
    user.check_name()

    logging.info(f'Пользователь {message.from_user.first_name} {message.from_user.last_name} залогинился')

    await message.answer("Привет! Этот бот сравнивает позволяет сравнить фамилии по "
                         "<a href='https://ru.wikipedia.org/wiki/"
                         "%D0%A0%D0%B5%D0%B9%D1%82%D0%B8%D0%BD%D0%B3_%D0%AD%D0%BB%D0%BE'>рейтингу Эло.</a> "
                         "Для перечня команд набери /help", parse_mode=types.ParseMode.HTML)


async def helping_message(message: types.Message):
    """
    Сообщение выводит существующие команды

    :param message: сообщение
    """
    await message.answer(fmt.text("Я знаю следующие команды:", "/rate - выбрать более смешного из пары",
                                  "/rating - показать список лидеров", sep='\n'))


def register_handlers_common(dp: Dispatcher):
    """
    Регистрация основных сообщений в диспетчере

    :param dp: диспетчер
    """
    dp.register_message_handler(starting_message, commands="start", state="*")
    dp.register_message_handler(helping_message, commands="help")
