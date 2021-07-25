from aiogram import Dispatcher, types

import seaborn as sns
import matplotlib.pyplot as plt
import logging
import os

from .. import dbworker

sns.set()
sns.set(rc={'figure.figsize': (15, 7)})


async def see_rating(message: types.Message):
    """
    Функция отправки изображения с рейтингом

    :param message: сообщение
    """
    top5 = dbworker.dbase.execute_query('select fio, rating from names.default_names order by rating desc limit 5'
                                        , with_result=True)
    sns.barplot(x='rating', y='fio', data=top5,  palette="Blues_d")
    file_name = f'test_{message.from_user.id}.png'
    plt.savefig(file_name)

    logging.info(f'Пользователь {message.from_user.first_name} {message.from_user.last_name} смотрит рейтинг')

    await message.answer_photo(photo=open(file_name, 'rb'))
    os.remove(file_name)


def register_handlers_rating(dp: Dispatcher):
    """
    Регистрация графических сообщений в диспетчере

    :param dp: диспетчер
    """
    dp.register_message_handler(see_rating, commands="rating")
