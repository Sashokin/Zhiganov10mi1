# -*- coding: utf-8 -*-
import config
import telebot
from telebot import types
import my_markups
import config_for_token
import sqlite3


bot = telebot.TeleBot(config_for_token.token)


conn = sqlite3.connect('global.db')
c = conn.cursor()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Привет! Я бот магазина metoyou!😊')
    bot.send_photo(message.chat.id, open('teddybears/start.jpg', 'rb'))
    bot.send_message(message.chat.id, 'Главное меню', reply_markup=my_markups.main_menu)


@bot.message_handler(commands=['help'])
def send_help(message):
    comtxt = open('commands.txt', encoding='utf-8')
    bot.send_message(message.chat.id, '📌Список команд:\n\n{}\n\nВыберите ниже раздел справки и получите всю необходимую информацию. Если вопрос не решен, обратитесь сюда: @glhflll'.format(comtxt.read()), reply_markup=my_markups.help_page)


@bot.message_handler(commands=['main'])
def main_menu(message):
    bot.send_message(message.chat.id, 'Главное меню', reply_markup=my_markups.main_menu)


@bot.message_handler(commands=['personal'])
def main_menu(message):
    bot.send_message(message.chat.id, 'Персональные данные', reply_markup=my_markups.personal_page)


@bot.message_handler(commands=['changepersonal'])
def cmd_change(message):
    pass
#    state = dbworker.get_current_state(message.chat.id)
 #   if state == config.States.S_ENTER_GEO.value:
  #      bot.send_message(message.chat.id, 'Нажмите на кнопку, чтобы мы смогли получить Ваш номер телефона и местоположение(для дальнейшей доставки)', reply_markup=my_markups.geophone_page)
   # else:
    #    bot.send_message(message.chat.id, 'Введите, пожалуйста, Ваше имя')
     #   dbworker.set_state(message.chat.id, config.States.S_ENTER_NAME.value)


@bot.message_handler(commands=['resetpersonal'])
def cmd_change(message):
    pass
#    dbworker.set_state(message.chat.id, config.States.S_START.value)
#    bot.send_message(message.chat.id, 'Вы сбросили персональные данные, чтобы внести их, используйте /changepersonal', reply_markup=my_markups.go_to_main_menu)


@bot.message_handler(content_types=['text'])
def main_menu(message):
    if message.text == '🚪Главное меню' or message.text == '🚪Вернуться в главное меню':
        bot.send_message(message.chat.id, 'Главное меню', reply_markup=my_markups.main_menu)
    elif message.text == '❓Помощь и связь' or message.text == '❓Помощь':
        comtxt = open('commands.txt', encoding='utf-8')
        bot.send_message(message.chat.id, 'Список команд:\n\n{}\n\nВыберите ниже раздел справки и получите всю необходимую информацию. Если вопрос не решен, обратитесь сюда: @glhflll'.format(comtxt.read()), reply_markup=my_markups.help_page)
    elif message.text == '📋Информация на сайте':
        bot.send_message(message.chat.id, 'Если информации на сайте недостаточно, свяжитесь с нами', reply_markup=my_markups.to_site)
        bot.send_message(message.chat.id, 'Связаться с нами', reply_markup=my_markups.help_page_out_site)
    elif message.text == '📞Позвонить':
        bot.send_message(message.chat.id, '📞 +7(916)204-12-22\n\nГрафик работы:\nБудни 9:00-21:00\nСуббота 10:00-19:00', reply_markup=my_markups.help_page)
    elif message.text == '⌨️Написать':
        bot.send_message(message.chat.id, 'Напиишите свое сообщение, оно сразу будет передано нам', reply_markup=my_markups.help_page)
    elif message.text == '👤Персональные данные':
        bot.send_message(message.chat.id, 'Персональные данные', reply_markup=my_markups.personal_page)
    elif message.text == '🔏Изменить персональные данные':
        bot.send_message(message.chat.id, 'Чтобы изменить персональные данные, используйте /changepersonal', reply_markup=my_markups.go_to_main_menu)
    elif message.text == '🐻Мишки':
        bot.send_message(message.chat.id, 'По какому параметру сортировать медведей?', reply_markup=my_markups.sort_page)
    elif message.text == '📏По размеру':
        bot.send_message(message.chat.id, 'Выберите размер мишки', reply_markup=my_markups.medved_page)
    elif message.text == '🛒Выбрать товар':
        bot.send_message(message.chat.id, 'Выберите интересующий товар и нажмите на соответствующую кнопку😊', reply_markup=my_markups.menu_page)
    elif message.text == '🔮Разное':
        bot.send_message(message.chat.id, 'Извините, товаров этой категории нет в наличии😔', reply_markup=my_markups.no_goods_page)
    elif message.text == '🎈Товары со скидкой':
        bot.send_message(message.chat.id, 'Извините, товаров этой категории нет в наличии😔', reply_markup=my_markups.no_goods_page)
    elif message.text == '🐻7-18 сантиметров🐻':
        bot.send_message(message.chat.id, c.execute('SELECT theme FROM goods WHERE size_type = 1').fetchall())
    else:
        comtxt = open('commands.txt', encoding='utf-8')
        bot.send_message(message.chat.id, '😟Не понимаю Вас, вот список команд:\n\n{}\n\n'.format(comtxt.read()), reply_markup=my_markups.go_to_main_menu)


@bot.message_handler(content_types=['sticker', 'pinned_message', 'photo', 'audio', 'document'])
def answer_not_a_text(message):
    comtxt = open('commands.txt', encoding='utf-8')
    bot.send_message(message.chat.id, '😟Не могу никак на это ответить, вот список команд\n\n{}\n\n'.format(comtxt.read()), reply_markup=my_markups.go_to_main_menu)


if __name__ == '__main__':
    bot.polling(none_stop=True)
