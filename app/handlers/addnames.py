from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import IDFilter
from aiogram.dispatcher.filters.state import State, StatesGroup

import re

from .. import dbworker


class OrderAddNames(StatesGroup):
    """
    Класс состояний конечных автоматов

    """
    waiting_for_name = State()


async def start_adding_new_name(message: types.Message):
    """
    Функция позволяет админу добавить новые имена, здесь идет ожидание ввода имени

    :param message: сообщение
    """
    await message.answer("Вы открыли админскую команду по добавлению новых имен. Введите имя и фамилию")
    await OrderAddNames.waiting_for_name.set()


async def adding_new_name(message: types.Message, state: FSMContext):
    """
    Функция предоставлляет админу возможность добавить новое имя

    :param message: сообщение
    :param state: состоояние
    """
    new_name = message.text.lower()

    if bool(re.search('[a-z]', new_name)):
        await message.answer("Пожалуйста, ввыдеите имя, используя кириллические символы.")
        return
    elif not dbworker.dbase.execute_query(query=f"select fio from names.default_names where id = "
                                                f"md5('{message.text}')::bytea", with_result=True).empty:
        await message.answer("Такое имя уже есть!")
        await state.finish()
        return

    dbworker.dbase.execute_query(
        query=f"insert into names.pairs select md5('{message.text}' || '-' || fio)::bytea, \
                    '{message.text}' || '-' || fio, ARRAY[]::integer[] from names.default_names; \
              insert into names.default_names values (md5('{message.text}')::bytea, '{message.text}', 0, 0);"
    )

    await message.reply("Принято!")
    await state.finish()


def register_handlers_add_names(dp: Dispatcher):
    """
    Регистрация сообщений в диспетчере

    :param dp: диспетчер
    """
    dp.register_message_handler(start_adding_new_name, IDFilter(user_id=367318262), commands="add_name")
    dp.register_message_handler(adding_new_name, IDFilter(user_id=367318262), state=OrderAddNames.waiting_for_name)
