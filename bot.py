import math
import telebot
from telebot import types
from CovidTracker import CovidTracker

TOKEN = '1602896092:AAG-1gj1jcPgRZB-OKLBSi--fmsbWweMq6w'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('Во всём мире')
    btn2 = types.KeyboardButton('Беларусь')
    btn3 = types.KeyboardButton('Россия')
    btn4 = types.KeyboardButton('Украина')
    markup.add(btn1, btn2, btn3, btn4)

    replyMsg = "Привет <b>{message.from_user.first_name}</b>\n" \
               "Я бот <b>Covid Tracker</b> - слежу за данными по коронавирусу.\n" \
               "\n<b>Как пользоваться</b>\n" \
               "Напиши название страны, к примеру <b>США</b> или <b>Германия</b>, " \
               "и я расскажу, как там обстоят дела. В ответ на <b>В мире</b> сообщу данные по всему миру. " \
               "Популярные страны видны на кнопках.\n" \
               "\n<b>Мои команды</b>\n" \
               "/start - вновь покажет это сообщение\n" \
               "/list  - список стран, за которыми я слежу\n" \
               "/info  - о точности, источниках и прочем\n" \
               "\n<i>Источник данных: JHU CSSE</i>"
    bot.send_message(message.chat.id, replyMsg, parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['info'])
def send_welcome(message):
    replyMsg = '<b>Источники</b>\n' \
               'Основной источник данных - CSSE Data Repository at Johns Hopkins University, ' \
               'который является репозиторием данных, предоставленных WHO, ECDC, US CDC и другими организациями.\n' \
               '\n<b>Точность</b>\n' \
               'По разным причинам не по всем странам есть возможность получить точные и актуальные данные, ' \
               'и иногда возникает ситуация, когда для некоторых стран данные либо отсутствуют, ' \
               'либо не актуальны.\n' \
               '\n<b>Выбор страны</b>\n' \
               'Страну можно выбрать несколькими способами:\n' \
               '1. По названию на русском  —  <b>Япония</b>\n' \
               '2. По английскому названию  —  <b>Japan</b>\n' \
               '3. По двухбуквенному коду (ISO 3166)  —  <b>JP</b>\n' \
               'Для некоторых стран существуют алиасы: <b>США</b>, <b>Америка</b>, <b>Соединенные Штаты</b> ' \
               '— всё это одна страна'
    bot.send_message(message.chat.id, replyMsg, parse_mode='html')


@bot.message_handler(commands=['list'])
def send_welcome(message):
    tracker = CovidTracker()
    countriesList = tracker.getCountriesList()
    height = math.ceil(len(countriesList) / 2)

    i = 0
    str = ''
    while i < height:
        str += "{:<16}".format(countriesList[i])
        try:
            str += countriesList[i + height]
        except:
            pass
        str += '\n'
        i += 1

    replyMsg = '<b>Вот список стран, за которыми я слежу:</b>\n<pre>' + str + '</pre>'
    bot.send_message(message.chat.id, replyMsg, parse_mode='html')


@bot.message_handler(content_types=['text'])
def mess(message):
    replyMsg = ""
    userText = message.text.strip().lower()
    userText = userText.replace("ё", "е")
    tracker = CovidTracker()

    # World data
    if userText in ['во всем мире', 'в мире', 'по всему миру', 'по миру', 'мир', 'world']:
        data = tracker.getData('world', 'text')
        replyMsg += 'Данные по <b>всему миру</b>:\n' \
                    '<pre>-----------------------------------\n' \
                    + data + '</pre>'

    # Country data
    else:
        country = tracker.processCountryName(userText)
        if not country:
            replyMsg = 'Страна "<b>' + message.text + '</b>" не найдена\n'
        else:
            data = tracker.getData(country['code'], 'text')
            replyMsg = 'Данные по стране <b>' + country['name'] + '</b>:\n' \
                       '<pre>-----------------------------------\n' \
                       + data + '</pre>'

    bot.send_message(message.chat.id, replyMsg, parse_mode='html')


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Не пойму что это значит")


bot.polling(none_stop=True)
