# -*- coding: utf-8 -*-
import config
import telebot
import time
from telebot import types
import my_markups


bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Привет! Я бот магазина metoyou!', reply_markup=my_markups.to_site)
    bot.send_message(message.chat.id, 'Воспользуйтесь клавиатурой, чтобы перейти в главное меню', reply_markup=my_markups.go_to_main_menu)


@bot.message_handler(commands=['help'])
def send_help(message):
    f = open('commands.txt', encoding='utf-8')
    bot.send_message(message.chat.id, 'Список команд:\n{}\n\nВыберите ниже раздел справки и получите всю необходимую информацию. Если вопрос не решен, обратитесь сюда: @glhflll'.format(f.read()), reply_markup=my_markups.help_page)


@bot.message_handler(commands=['main'])
def main_menu(message):
    bot.send_message(message.chat.id, 'Главное меню', reply_markup=my_markups.main_menu)


@bot.message_handler(content_types=["text"])
def main_menu(message):
    if message.text == 'Главное меню' or message.text == 'Вернуться в главное меню':
        bot.send_message(message.chat.id, 'Главное меню', reply_markup=my_markups.main_menu)
    elif message.text == 'Помощь и связь' or message.text == 'Помощь':
        f = open('commands.txt', encoding='utf-8')
        bot.send_message(message.chat.id, 'Список команд:\n{}\n\nВыберите ниже раздел справки и получите всю необходимую информацию. Если вопрос не решен, обратитесь сюда: @glhflll'.format(f.read()), reply_markup=my_markups.help_page)
    elif message.text == 'Информация на сайте':
        bot.send_message(message.chat.id, 'Если информации на сайте недостаточно, свяжитесь с нами', reply_markup=my_markups.to_site)
        bot.send_message(message.chat.id, 'Связаться с нами', reply_markup=my_markups.help_page_out_site)
    elif message.text == 'Позвонить':
        bot.send_message(message.chat.id, '+7(916)204-12-22\n\nГрафик работы:\nБудни 9:00-21:00\nСуббота 10:00-19:00', reply_markup=my_markups.help_page)
    elif message.text == 'Написать':
        bot.send_message(message.chat.id,'По всем вопросам: @glhflll', reply_markup=my_markups.help_page)
    else:
        bot.send_message(message.chat.id, "Не понимаю Вас. Нажмите на кнопку для перехода на наш сайт.", reply_markup=my_markups.to_site)
        bot.send_message(message.chat.id, 'Или перейдите в главное меню', reply_markup=my_markups.go_to_main_menu)


@bot.message_handler(content_types=["sticker", "pinned_message", "photo", "audio", 'document'])
def answer_not_a_text(message):
    bot.send_message(message.chat.id, "Не могу никак на это ответить, перейти в главное меню?", reply_markup=my_markups.go_to_main_menu)


if __name__ == '__main__':
    bot.polling(none_stop=True)
