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
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button = types.KeyboardButton('Главное меню')
    markup.add(button)
    bot.send_message(message.chat.id, 'Привет! Я бот магазина metoyou!', reply_markup=keyboard)
    bot.send_message(message.chat.id, 'Воспользуйтесь клавиатурой, чтобы перейти в главное меню', reply_markup=markup)


@bot.message_handler(content_types=["text"])
def main_menu(message):
    if message.text == 'Главное меню':
        bot.send_message(message.chat.id, 'Это главное меню')
    else:
        keyboard = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(text="Перейти на сайт", url="www.metoyou-shop.ru")
        keyboard.add(url_button)
        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button = types.KeyboardButton('Главное меню')
        markup.add(button)
        bot.send_message(message.chat.id, "Не понимаю Вас. Нажмите на кнопку для перехода на наш сайт.", reply_markup=keyboard)
        bot.send_message(message.chat.id, 'Или перейдите в главное меню', reply_markup=markup)


@bot.message_handler(content_types=["sticker", "pinned_message", "photo", "audio", 'document'])
def answer_not_a_text(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button = types.KeyboardButton('Главное меню')
    markup.add(button)
    bot.send_message(message.chat.id, "Не могу никак на это ответить, перейти на главное меню?", reply_markup=markup)


if __name__ == '__main__':
    bot.polling(none_stop=True)
