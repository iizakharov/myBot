import datetime

import telebot
import config
import random
from telebot import types

from telebot import apihelper


bot = telebot.TeleBot(config.TOKEN)
# apihelper.proxy = {'http': 'http://11ce8230.ngrok.io'}
# apihelper.proxy = {'https': 'socks4://userproxy:password@109.87.183.226:4145'}


@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('static/welcome.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)

    #  клавиатура
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Рандомное число')
    item2 = types.KeyboardButton('Как дела?')

    markup.add(item1, item2)

    bot.send_message(message.chat.id, 'Какие люди в Голливуде!? '
                                      '\n{0.first_name}, я - <b>{1.first_name}'
                                      '</b>, бот созданный чтобы быть'
                                      ' подопытным.'.format(message.from_user,
                                                            bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['sticker'])
def stick_aswer(message):
    bot.send_message(message.chat.id, 'Вау какой крутой стикер!!!')


@bot.message_handler(content_types=['text'])
def dialog(message):
    if message.chat.type == 'private':
        if message.text == 'Рандомное число':
            # bot.send_message(message.chat.id, str(random.randint(0, 100)))
            date = datetime.datetime.now()
            bot.send_message(message.chat.id, date.strftime('%d-%m-%Y %H:%M'))
        elif message.text == 'Как дела?':
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton('Хорошо', callback_data='good')
            item2 = types.InlineKeyboardButton('Не очень', callback_data='bad')

            markup.add(item1, item2)

            bot.send_message(message.chat.id, 'Отлично! Как сам?',
                             reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Не знаю что ответить :( ')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Вот и отличненько :)')
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Бывает :( ')

            # remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text='Как дела?', reply_markup=None)
            # show alert
            bot.answer_callback_query(callback_query_id=call.id,
                                      show_alert=False,
                                      text="ЭТО ТЕСТОВОЕ УВЕДОМЛЕНИЕ!!11")
    except Exception as e:
        print(repr(e))


# RUN
bot.polling(none_stop=True)