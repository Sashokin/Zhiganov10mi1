# -*- coding: utf-8 -*-
import config
import telebot
import time
from telebot import types


bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text="Перейти на сайт", url="www.metoyou-shop.ru")
    keyboard.add(url_button)
    bot.send_message(message.chat.id, 'Привет! Я бот магазина metoyou!', reply_markup=keyboard)


@bot.message_handler(content_types=["text"])
def default_test(message):
    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text="Перейти на сайт", url="www.metoyou-shop.ru")
    keyboard.add(url_button)
    bot.send_message(message.chat.id, "В данный момент бот находится в стадии проектирования. Нажми на кнопку для перехода на наш сайт.", reply_markup=keyboard)


if __name__ == '__main__':
    bot.polling(none_stop=True)
