import logging
import os
import pytz

from telegram import ReplyKeyboardMarkup
from telegram.ext import ConversationHandler

LOGGER = logging.getLogger(__name__)

DATABASE_URL = os.environ['DATABASE_URL']

TOKEN = os.environ['TOKEN']
HOST = os.environ['HOST']
PORT = os.environ['PORT']
URL = os.environ['URL']
TZ = os.environ['TZ']

TIMEZONE = pytz.timezone(TZ)

DEFAULT_TIMESETTING = os.environ['DEFAULT_TIMESETTING']
CREATOR_ID = int(os.environ['CREATOR_ID'])
CREATOR_USERNAME = os.environ['CREATOR_USERNAME']
TYSOVKA_ID = int(os.environ['TYSOVKA_ID'])

REPO_URL = os.environ['REPO_URL']

START_KEYBOARD = [['подписка']]
DEFAULT_KEYBOARD = [['подписка', 'отписка'],
                    ['люди', 'время'],
                    ['настройки', 'отмена']]
CREATOR_KEYBOARD = [['подписка', 'отписка'],
                    ['люди', 'время'],
                    ['настройки', 'праздники'],
                    ['отмена']]
OPTIONS_KEYBOARD = [['да', 'нет']]
GENDER_KEYBOARD = [['мужской', 'женский']]
CHANGE_KEYBOARD = [['имя'],
                   ['пол'],
                   ['дата рождения']]

START_MARKUP = ReplyKeyboardMarkup(START_KEYBOARD)
DEFAULT_MARKUP = ReplyKeyboardMarkup(DEFAULT_KEYBOARD)
CREATOR_MARKUP = ReplyKeyboardMarkup(CREATOR_KEYBOARD)
OPTIONS_MARKUP = ReplyKeyboardMarkup(OPTIONS_KEYBOARD)
GENDER_MARKUP = ReplyKeyboardMarkup(GENDER_KEYBOARD)
CHANGE_MARKUP = ReplyKeyboardMarkup(CHANGE_KEYBOARD)

USERNAME_STORED, GENDER_STORED, BIRTHDAY_STORED = range(0, 3)
TIME_ENTERED, TIME_REPEATED = range(3, 5)
SETTING_CHOSEN = 5
HOLIDAY_ADDED = 6
END = ConversationHandler.END
