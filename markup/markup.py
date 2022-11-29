from telebot.types import KeyboardButton
from settings import config
from data_base.dbalchemy import DBManager


class Keyboards:
    """
    Класс предназначен для создания и разметки интерфейса бота
    """

    def __init__(self):
        self.markup = None
        self.DB = DBManager

    def set_btn(self, name, step=0, quantity=0):
        """
        Создает и возвращает кнопку по входным параметрам
        """

        return KeyboardButton(config.KEYBOARD[name])
