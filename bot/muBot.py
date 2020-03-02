import datetime
import telebot
import config
import logging
from telebot import types
from create_db import create_table, add_summ, i_got, count, get_all
from config import MONTHS, TRANSLATE
from utils import get_key

logger = logging.getLogger('muBot')

bot = telebot.TeleBot(config.TOKEN)
date = datetime.datetime.now()
month = date.strftime('%B_%Y')


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
    item5 = types.KeyboardButton('Глянуть в прошлое')

    markup.add(item1, item2, item3, item4, item5)

    bot.send_message(message.chat.id, 'Какие люди в Голливуде!?'
                                      '\n{0.first_name}, я - <b>{1.first_name}'
                                      '</b>, бот созданный чтобы быть'
                                      ' полезным ;) '.format(message.from_user,
                                                             bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['help'])
def welcome(message):
    sti = open('static/help.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)

    bot.send_message(message.chat.id, 'Ой {0.first_name}, у тебя трудности?'
                                      '\nЕсли хочешь поработать, напиши в'
                                      ' чат:\n/start\n и тогда пообщаемся {1}'
                     .format(message.from_user, u"\U0001F618"),
                     parse_mode='html')


@bot.message_handler(content_types=['sticker'])
def stick_answer(message):
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
                bot.send_message(message.chat.id, 'Эм... \n' + str(summa) +
                                 ' братка')
            except Exception as e:
                logger.error('Ошибка вывода общей суммы: ' + repr(e))
                bot.send_message(message.chat.id,
                                 'Новый месяц ещё не заведен в базе :(\nЖмакай'
                                 ' на кнопку "Новый месяц"')
        elif message.text == 'Новый месяц':
            try:
                create_table(table_name)
                bot.send_message(message.chat.id, 'Готово!\nНовый месяц "'
                                 + str(table_name) + '" дабавлен ;)')
            except Exception as e:
                logger.error('Ошибка создания таблицы: ' + repr(e))
                bot.send_message(message.chat.id,
                                 'Этот месяц "' + table_name + '" уже создан')
        elif message.text == 'Глянуть в прошлое':
            all_month_before = []
            items_to_markup = []
            now_month = date.strftime('%m')
            this_year = date.strftime('%Y')
            markup = types.InlineKeyboardMarkup(row_width=2)

            for i in range(1, int(now_month)):
                all_month_before.append('{0}_{1}_{2.id}'
                                        .format(MONTHS[i],
                                                this_year,
                                                message.from_user)
                                        )
                items_to_markup.append(f'item{i}')
                items_to_markup[i-1] = types.InlineKeyboardButton(
                    f'{TRANSLATE[MONTHS[i]]}',
                    callback_data=f'{TRANSLATE[MONTHS[i]]}')
                markup.add(items_to_markup[i-1])
            bot.send_message(message.chat.id, 'Вебери месяц:',
                             reply_markup=markup)

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
                    elif (int(message.text) >= 500)and(int(message.text)
                                                       < 1000):
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
                    # print('Ошибка ввода сообщения: ' + repr(e))
                    logger.error('Ошибка ввода сообщения: ' + repr(e))
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
                bot.send_message(call.message.chat.id,
                                 'Всего: ' + str(count(table_name)) +
                                 ' движений')
            elif call.data == 'all':
                bot.send_message(call.message.chat.id, get_all(table_name))

            elif call.data in TRANSLATE.values():
                val = get_key(TRANSLATE, call.data)
                table = '{0}_{1}_{2.id}'.format(val, date.strftime('%Y'),
                                                call.from_user)
                try:
                    bot.send_message(call.message.chat.id, get_all(table))
                    bot.send_message(call.message.chat.id,
                                     'Всего: ' + str(i_got(table)))
                except Exception as e:
                    logger.error('Ошибка запроса. Несуществующий месяц '
                                 + repr(e))
                    bot.send_message(call.message.chat.id,
                                     'В том месяце голяк.. Выбери другой!')

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
        # print('Ошибка callback_query: ' + repr(e))
        logger.error('Ошибка callback_query: ' + repr(e))


# RUN
bot.polling(none_stop=True)
