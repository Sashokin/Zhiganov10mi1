# -*- coding: utf-8 -*-
import config
import telebot
from telebot import types
import my_markups
import config_for_token
import sqlite3


bot = telebot.TeleBot(config_for_token.token)

cursor = config.conn.cursor()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Привет! Я бот магазина metoyou!', reply_markup=my_markups.to_site)
    bot.send_message(message.chat.id, 'Воспользуйтесь клавиатурой, чтобы перейти в главное меню', reply_markup=my_markups.go_to_main_menu)


@bot.message_handler(commands=['help'])
def send_help(message):
    comtxt = open('commands.txt', encoding='utf-8')
    bot.send_message(message.chat.id, 'Список команд:\n\n{}\n\nВыберите ниже раздел справки и получите всю необходимую информацию. Если вопрос не решен, обратитесь сюда: @glhflll'.format(comtxt.read()), reply_markup=my_markups.help_page)


@bot.message_handler(commands=['main'])
def main_menu(message):
    bot.send_message(message.chat.id, 'Главное меню', reply_markup=my_markups.main_menu)


@bot.message_handler(commands=['personal'])
def main_menu(message):
    bot.send_message(message.chat.id, 'Персональные данные', reply_markup=my_markups.personal_page)


@bot.message_handler(content_types=['text'])
def main_menu(message):
    if message.text == 'Главное меню' or message.text == 'Вернуться в главное меню':
        bot.send_message(message.chat.id, 'Главное меню', reply_markup=my_markups.main_menu)
    elif message.text == 'Помощь и связь' or message.text == 'Помощь':
        comtxt = open('commands.txt', encoding='utf-8')
        bot.send_message(message.chat.id, 'Список команд:\n\n{}\n\nВыберите ниже раздел справки и получите всю необходимую информацию. Если вопрос не решен, обратитесь сюда: @glhflll'.format(comtxt.read()), reply_markup=my_markups.help_page)
    elif message.text == 'Информация на сайте':
        bot.send_message(message.chat.id, 'Если информации на сайте недостаточно, свяжитесь с нами', reply_markup=my_markups.to_site)
        bot.send_message(message.chat.id, 'Связаться с нами', reply_markup=my_markups.help_page_out_site)
    elif message.text == 'Позвонить':
        bot.send_message(message.chat.id, '+7(916)204-12-22\n\nГрафик работы:\nБудни 9:00-21:00\nСуббота 10:00-19:00', reply_markup=my_markups.help_page)
    elif message.text == 'Написать':
        bot.send_message(message.chat.id, 'По всем вопросам: @glhflll', reply_markup=my_markups.help_page)
    elif message.text == 'Персональные данные':
        bot.send_message(message.chat.id, 'Персональные данные', reply_markup=my_markups.personal_page)
    elif message.text == 'Изменить персональные данные':
        bot.send_message(message.chat.id, 'Чтобы изменить персональные данные, используйте /changepersonal', reply_markup=my_markups.go_to_main_menu)
    else:
        comtxt = open('commands.txt', encoding='utf-8')
        bot.send_message(message.chat.id, 'Не понимаю Вас, вот список команд:\n\n{}\n\n'.format(comtxt.read()), reply_markup=my_markups.go_to_main_menu)


@bot.message_handler(content_types=['sticker', 'pinned_message', 'photo', 'audio', 'document'])
def answer_not_a_text(message):
    comtxt = open('commands.txt', encoding='utf-8')
    bot.send_message(message.chat.id, 'Не могу никак на это ответить, вот список команд\n\n{}\n\n'.format(comtxt.read()), reply_markup=my_markups.go_to_main_menu)


if __name__ == '__main__':
    bot.polling(none_stop=True)
