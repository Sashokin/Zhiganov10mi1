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


@bot.message_handler(content_types=["text"])
def main_menu(message):
    if message.text == 'Главное меню':
        bot.send_message(message.chat.id, 'Главное меню', reply_markup=my_markups.main_menu)
    else:
        bot.send_message(message.chat.id, "Не понимаю Вас. Нажмите на кнопку для перехода на наш сайт.", reply_markup=my_markups.to_site)
        bot.send_message(message.chat.id, 'Или перейдите в главное меню', reply_markup=my_markups.go_to_main_menu)


@bot.message_handler(content_types=["sticker", "pinned_message", "photo", "audio", 'document'])
def answer_not_a_text(message):
    bot.send_message(message.chat.id, "Не могу никак на это ответить, перейти в главное меню?", reply_markup=my_markups.go_to_main_menu)


if __name__ == '__main__':
    bot.polling(none_stop=True)
