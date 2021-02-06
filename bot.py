import telebot
from telebot import types
from CovidTracker import CovidTracker

TOKEN = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('Во всём мире')
    btn2 = types.KeyboardButton('Беларусь')
    btn3 = types.KeyboardButton('Россия')
    btn4 = types.KeyboardButton('Украина')
    markup.add(btn1, btn2, btn3, btn4)

    send_message = f"Привет <b>{message.from_user.first_name}</b>\n" \
                   f"Я бот <b>Covid Tracker</b> - слежу за данными по коронавирусу\n" \
                   f"Напиши страну или \"<b><code>В мире</code></b>\" и я расскажу, как там обстоят дела\n" \
                   f"Источник данных: <i>JHU CSSE</i>" \
                   # f"Вот некоторые полезные команды:\n" \
                   # f"/start - Приветствие\n" \
                   # f"/help - Помощь\n" \
                   # f"/countries - Список стран, за которыми я слежу\n" \

    bot.send_message(message.chat.id, send_message, parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Это раздел помощи", parse_mode='html')


@bot.message_handler(commands=['countries'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Список стран, за которыми я слежу:", parse_mode='html')


@bot.message_handler(content_types=['text'])
def mess(message):
    replyMsg = ""
    userText = message.text.strip().lower()
    tracker = CovidTracker()

    # World data
    if userText in ['во всём мире', 'в мире', 'по всему миру', 'по миру', 'мир', 'world']:
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
