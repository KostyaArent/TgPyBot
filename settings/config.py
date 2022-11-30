import os
from emoji import emojize
from decouple import config


TG_TOKEN = config('TG_TOKEN')
NAME_DB = config('NAME_DB')
VERSION = '0.0.1'
AUTHOR = 'KostyaArent'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join('sqlite:///'+BASE_DIR, NAME_DB)

COUNT = 0

# кнопки управления
KEYBOARD = {
    'CHOOSE_GOODS': emojize(':open_file_folder: Выбрать товар'),
    'INFO': emojize(':speech_balloon: О магазине'),
    'SETTINGS': emojize('⚙️ Настройки'),
    'PIZZA': emojize(':pizza: Пицца', language='alias'),
    'ICE_CREAM': emojize(':shaved_ice: Мороженое', language='alias'),
    'COFFEE': emojize(':coffee: Кофе', language='alias'),
    '<<': emojize('⏪'),
    '>>': emojize('⏩'),
    'BACK_STEP': emojize('◀️'),
    'NEXT_STEP': emojize('▶️'),
    'ORDER': emojize('✅ ЗАКАЗ'),
    'X': emojize('❌'),
    'DOUWN': emojize('🔽'),
    'AMOUNT_PRODUCT': COUNT,
    'AMOUNT_ORDERS': COUNT,
    'UP': emojize('🔼'),
    'APPLAY': '✅ Оформить заказ',
    'COPY': '©️'
}

# id категорий продуктов
CATEGORY = {
    'PIZZA': 1,
    'ICE_CREAM': 2,
    'COFFEE': 3,
}

# названия команд
COMMANDS = {
    'START': "start",
    'HELP': "help",
}