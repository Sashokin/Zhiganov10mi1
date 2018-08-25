# -*- coding: utf-8 -*-
import config
import telebot
from telebot import types
import my_markups
import config_for_token
from peewee import *
import dbhelp
import time
#todo: сортировка медведей по тематике, корзина, красивый вывод фото+текст

bot = telebot.TeleBot(config_for_token.token)


#db = SqliteDatabase('database.db')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    ccid = message.chat.id
    cb = 0
    for p in dbhelp.User.select():
        if int(p.cid) == ccid:
            cb = 1
    if cb == 0:
        ccid = dbhelp.User(cid=ccid, type='0', name='none', phone='none', uvedl='1', orders='none', sendmes='0')
        ccid.save()
        bot.send_photo(message.chat.id, open('teddybears/start.jpg', 'rb'))
        bot.send_message(message.chat.id, 'Привет!😊 Я бот магазина metoyou! А тебя я еще не знаю😔', reply_markup=my_markups.start_page)
    else:
        for p in dbhelp.User.select():
            if int(p.cid) == ccid:
                if p.name == 'none':
                    bot.send_message(message.chat.id, 'Привет!😊 Я бот магазина metoyou! А тебя я до сих пор не знаю😔', reply_markup=my_markups.start_page)
                else:
                    bot.send_message(message.chat.id, 'Привет, {} 😊'.format(p.name), reply_markup=my_markups.main_menu)


@bot.message_handler(commands=['help'])
def send_help(message):
    comtxt = open('commands.txt', encoding='utf-8')
    bot.send_message(message.chat.id, '📌Список команд:\n\n{}\n\nВыберите ниже раздел справки'.format(comtxt.read()), reply_markup=my_markups.help_page)


@bot.message_handler(commands=['main'])
def main_menu(message):
    bot.send_message(message.chat.id, 'Главное меню', reply_markup=my_markups.main_menu)


@bot.message_handler(content_types=['text'])
def main(message):
    ccid = message.chat.id
    enter_name = 0
    enter_mes = 0
    for p in dbhelp.User.select():
        if str(p.cid) == str(ccid):
            if p.type == '1':
                enter_name = 1
            if p.sendmes == '1':
                enter_mes = 1
    if message.text == '❌Отмена':
        for p in dbhelp.User.select():
            if str(p.cid) == str(ccid):
                p.type = '0'
                p.save()
        bot.send_message(message.chat.id, 'Хорошо, вернемся к этому позже', reply_markup=my_markups.main_menu)
    if message.text == '❌Отменить':
        for p in dbhelp.User.select():
            if str(p.cid) == str(ccid):
                p.sendmes = '0'
                p.save()
        comtxt = open('commands.txt', encoding='utf-8')
        bot.send_message(message.chat.id, '📌Список команд:\n\n{}\n\nВыберите ниже раздел справки'.format(comtxt.read()), reply_markup=my_markups.help_page)
    elif enter_name == 1:
        for p in dbhelp.User.select():
            if str(p.cid) == str(ccid):
                p.name = message.text
                p.type = '2'
                bot.send_message(message.chat.id, 'Хорошо, {}, я запомнил😊'.format(p.name), reply_markup=my_markups.main_menu)
                p.save()
    elif enter_mes == 1:
        for p in dbhelp.User.select():
            if str(p.cid) == str(ccid):
                bot.send_message(680180012, '{}(@{} / @{}) оставил сообщение: \n{}'.format(p.name, message.from_user.username, message.chat.username, message.text))
                p.sendmes = '0'
                p.save()
                bot.send_message(message.chat.id, '⌨️Сообщение успешно доставлено', reply_markup=my_markups.help_page)
    elif message.text == '🚪Главное меню' or message.text == '🚪Вернуться в главное меню':
        bot.send_message(message.chat.id, 'Главное меню', reply_markup=my_markups.main_menu)
    elif message.text == '❓Помощь и связь' or message.text == '❓Помощь':
        comtxt = open('commands.txt', encoding='utf-8')
        bot.send_message(message.chat.id, '📌Список команд:\n\n{}\n\nВыберите ниже раздел справки'.format(comtxt.read()), reply_markup=my_markups.help_page)
    elif message.text == '📋Информация на сайте':
        bot.send_message(message.chat.id, 'Если информации на сайте недостаточно, свяжитесь с нами', reply_markup=my_markups.to_site)
        bot.send_message(message.chat.id, 'Связаться с нами', reply_markup=my_markups.help_page)
    elif message.text == '📞Позвонить':
        bot.send_message(message.chat.id, '📞 +7(916)204-12-22\n\nГрафик работы:\nБудни 9:00-21:00\nСуббота 10:00-19:00', reply_markup=my_markups.help_page)
    elif message.text == '⌨️Написать':
        bot.send_message(message.chat.id, 'Напишите свое сообщение, оно сразу будет передано нам', reply_markup=my_markups.enter_page2)
        for p in dbhelp.User.select():
            if str(p.cid) == str(ccid):
                p.sendmes = '1'
                p.save()
    elif message.text == '👤Персональные данные':
        bot.send_message(message.chat.id, 'Персональные данные', reply_markup=my_markups.personal_page)
    elif message.text == '🔏Ввести имя':
        bot.send_message(message.chat.id, 'Я запомню введенное имя', reply_markup=my_markups.enter_page)
        for p in dbhelp.User.select():
            if str(p.cid) == str(ccid):
                p.type = '1'
                p.save()
    elif message.text == '🐻Мишки':
        bot.send_message(message.chat.id, 'По какому параметру сортировать медведей?', reply_markup=my_markups.sort_page)
    elif message.text == '📏По размеру':
        bot.send_message(message.chat.id, 'Выберите размер мишки', reply_markup=my_markups.medved_page)
    elif message.text == '🛒Выбрать товар':
        bot.send_message(message.chat.id, 'Выберите интересующий товар и нажмите на соответствующую кнопку😊', reply_markup=my_markups.menu_page)
    elif message.text == '🔮Разное':
        bot.send_message(message.chat.id, 'Извините, товаров этой категории нет в наличии😔', reply_markup=my_markups.no_goods_page)
    elif message.text == 'Имя':
        for p in dbhelp.User.select():
            if str(p.cid) == str(ccid):
                bot.send_message(message.chat.id, 'Текущее имя: {} \nИзменить?'.format(p.name), reply_markup=my_markups.start_page)
    elif message.text == '🎈Товары со скидкой':
        for p in dbhelp.Product.select():
            if p.type == '1' and p.sale != '0':
                bot.send_message(message.chat.id, '🐻{}, {} см., {} рублей с учетом скидки'.format(p.name, p.size, p.price))
                bot.send_photo(message.chat.id, open('teddybears/{}.jpg'.format(p.theme), 'rb'),
                               reply_markup=check_available(p.available))
    elif message.text == '🐻10-18 сантиметров🐻':
        show_product('1', '1', message)
    elif message.text == '🐻20 сантиметров🐻':
        show_product('1', '2', message)
    elif message.text == '🐻23-25 сантиметров🐻':
        show_product('1', '3', message)
    elif message.text == '🐻30 сантиметров🐻':
        show_product('1', '4', message)
    elif message.text == '🐻40-50 сантиметров🐻':
        show_product('1', '5', message)
    elif message.text == '🎉По тематике':
        bot.send_message(message.chat.id, 'Раздел в разработке😔')
    elif message.text == '🎁Подарочные упаковки':
        for p in dbhelp.Product.select():
            if p.type == '2':
                bot.send_message(message.chat.id, '🎁{} {} см., {} рублей '.format(p.name, p.size, p.price))
                bot.send_photo(message.chat.id, open('teddybears/{}.jpg'.format(p.theme), 'rb'),
                               reply_markup=check_available(p.available))
    else:
        comtxt = open('commands.txt', encoding='utf-8')
        bot.send_message(message.chat.id, '😟Не понимаю Вас, вот список команд:\n\n{}\n\n'.format(comtxt.read()), reply_markup=my_markups.go_to_main_menu)


def check_available(a):
    mkup1 = types.InlineKeyboardMarkup()
    mkup2 = types.InlineKeyboardMarkup()
    mkbt1 = types.InlineKeyboardButton(text="✅Товар в наличии", callback_data="test")
    mkbt2 = types.InlineKeyboardButton(text="❌Товара нет в наличии", callback_data="test")
    mkup1.add(mkbt1)
    mkup2.add(mkbt2)
    if a == '1':
        return mkup1
    else:
        return mkup2


def show_product(product_type, size_type, message):
    for p in dbhelp.Product.select():
        if p.type == product_type and p.size_type == size_type:
            bot.send_message(message.chat.id, '🐻{}, {} см., {} рублей'.format(p.name, p.size, p.price))
            bot.send_photo(message.chat.id, open('teddybears/{}.jpg'.format(p.theme), 'rb'),
                           reply_markup=check_available(p.available))



@bot.message_handler(content_types=['sticker', 'pinned_message', 'photo', 'audio', 'document'])
def answer_not_a_text(message):
    comtxt = open('commands.txt', encoding='utf-8')
    bot.send_message(message.chat.id, '😟Не могу никак на это ответить, вот список команд\n\n{}\n\n'.format(comtxt.read()), reply_markup=my_markups.go_to_main_menu)


if __name__ == '__main__':
    bot.polling(none_stop=True)
