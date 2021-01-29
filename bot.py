import COVID19Py
import telebot
from config import conf



bot = telebot.TeleBot(conf["TOKEN"], parse_mode=None)