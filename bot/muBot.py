import datetime
import sqlite3
import telebot
import config
import random
from telebot import types
from create_db import create_table, add_summ, i_got, count, get_all

from telebot import apihelper


bot = telebot.TeleBot(config.TOKEN)
date = datetime.datetime.now()
month = date.strftime('%B_%Y')
# apihelper.proxy = {'http': 'http://11ce8230.ngrok.io'}
# apihelper.proxy = {'https': 'socks4://userproxy:password@109.87.183.226:4145'}


@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('static/welcome.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)

    #  клавиатура
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Стандартик')
    item2 = types.KeyboardButton('Чо по бабкам?')
    item3 = types.KeyboardButton('Новый месяц')
    item4 = types.KeyboardButton('Все движения')

    markup.add(item1, item2, item3, item4)

    bot.send_message(message.chat.id, 'Какие люди в Голливуде!?'
                                      '\n{0.first_name}, я - <b>{1.first_name}'
                                      '</b>, бот созданный чтобы быть'
                                      ' полезным ;) '.format(message.from_user,
                                                            bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['sticker'])
def stick_aswer(message):
    bot.send_message(message.chat.id, 'Вау какой крутой стикер!!!')


@bot.message_handler(content_types=['text'])
def dialog(message):
    if message.chat.type == 'private':
        table_name = '{0}_{1.id}'.format(month, message.from_user)
        if message.text == 'Стандартик':
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton('500', callback_data='500')
            item2 = types.InlineKeyboardButton('1000', callback_data='1000')
            markup.add(item1, item2)
            bot.send_message(message.chat.id, 'Сколько запишем?',
                             reply_markup=markup)
        elif message.text == 'Чо по бабкам?':
            try:
                summa = i_got(table_name)
                bot.send_message(message.chat.id, 'Эм... \n' + str(summa) + ' братка')
            except Exception as e:
                print('Ошибка вывода общей суммы: ' + repr(e))
                bot.send_message(message.chat.id,
                                 'Новый месяц ещё не заведен в базе :(\nЖмакай'
                                 ' на кнопку "Новый месяц"')
        elif message.text == 'Новый месяц':
            try:
                create_table(table_name)
                bot.send_message(message.chat.id, 'Готово!\nНовый месяц "'
                                 + str(table_name) + '" дабавлен ;)')
            except Exception as e:
                print('Ошибка создания таблицы: ' + repr(e))
                bot.send_message(message.chat.id,
                                 'Этот месяц "' + table_name + '" уже создан')

        elif message.text == 'Все движения':
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton('Cколько движений',
                                               callback_data='count')
            item2 = types.InlineKeyboardButton('Посмотреть всё',
                                               callback_data='all')

            markup.add(item1, item2)

            bot.send_message(message.chat.id, 'Сейчас всё расскажу..',
                             reply_markup=markup)

        else:
            if message.text:
                try:
                    if int(message.text) < 500:
                        add_summ(message.text, table_name)
                        bot.send_message(message.chat.id,
                                         'Мало!\nну сколько заработал {0}'
                                         .format(u"\U0001F595"))
                    elif int(message.text) >= 500 and int(message.text) < 1000:
                        add_summ(message.text, table_name)
                        bot.send_message(message.chat.id, message.text +
                                         ' номально вышло, но нужно подтянуть'
                                         ' до кЭсика')
                    elif int(message.text) >= 1000:
                        add_summ(message.text, table_name)
                        bot.send_message(message.chat.id, message.text +
                                         ' - вот номально вышло, умеешь же {0}'
                                         .format(u"\U0001F4AA"))
                except Exception as e:
                    print('Ошибка ввода сообщения: ' + repr(e))
                    bot.send_message(message.chat.id,
                                     'Нужно цыфры воодить! \nА если не создал '
                                     'новый месяц, то скорее жмакай на'
                                     ' одноименную кнопку')
            else:
                bot.send_message(message.chat.id, 'Не знаю что ответить :( ')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    table_name = '{0}_{1.id}'.format(month, call.from_user)
    try:
        if call.message:
            if call.data == 'count':
                summa = count(table_name)
                bot.send_message(call.message.chat.id,
                                 'Всего: ' + str(summa) + ' движений')
            elif call.data == 'all':
                all = get_all(table_name)
                bot.send_message(call.message.chat.id, all)

            elif call.data == '500':
                add_summ(500, table_name)
                bot.send_message(call.message.chat.id,
                                 'Пятиха... Ну не так уж и плохо :)')
            elif call.data == '1000':
                add_summ(1000, table_name)
                bot.send_message(call.message.chat.id, 'Касарик прилетел!')

            else:
                 bot.send_message(call.message.chat.id,
                                     'Миша, давай нпоновой! :( ')

            # remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text='Найс!', reply_markup=None)
            # show alert
            bot.answer_callback_query(callback_query_id=call.id,
                                      show_alert=False,
                                      text="Я ЗАПОМНИЛ ;) ")
    except Exception as e:
        print('Ошибка callback_query: ' + repr(e))


# RUN
bot.polling(none_stop=True)