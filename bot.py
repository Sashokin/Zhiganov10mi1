# -*- coding: utf-8 -*-
import config
import telebot
from telebot import types
import my_markups
import config_for_token
from peewee import *
import dbhelp
import time
#todo: сортировка медведей по тематике, красивый вывод фото+текст, проверить наличие+кол-во, удаление из корзины, доп предложения, оформление заказа

bot = telebot.TeleBot(config_for_token.token)


#db = SqliteDatabase('database.db')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    ccid = message.chat.id
    cb = 0
    for u in dbhelp.User.select():
        if str(u.cid) == str(ccid):
            cb = 1
    if cb == 0:
        ccid = dbhelp.User(cid=ccid, type='0', name='none', phone='none', uvedl='1', orders='none', sendmes='0', bin='none')
        ccid.save()
        bot.send_photo(message.chat.id, open('teddybears/start.jpg', 'rb'))
        bot.send_message(message.chat.id, 'Привет!😊 Я бот магазина metoyou! А тебя я еще не знаю😔', reply_markup=my_markups.start_page)
    else:
        for u in dbhelp.User.select():
            if str(u.cid) == str(ccid):
                if u.name == 'none':
                    bot.send_message(message.chat.id, 'Привет!😊 Я бот магазина metoyou! А тебя я до сих пор не знаю😔', reply_markup=my_markups.start_page)
                else:
                    bot.send_message(message.chat.id, 'Привет, {} 😊'.format(u.name), reply_markup=my_markups.main_menu)


@bot.message_handler(commands=['help'])
def send_help(message):
    comtxt = open('commands.txt', encoding='utf-8')
    bot.send_message(message.chat.id, '📌Список команд:\n\n{}\n\nВыберите ниже раздел справки'.format(comtxt.read()), reply_markup=my_markups.help_page)


@bot.message_handler(commands=['main'])
def main_menu(message):
    bot.send_message(message.chat.id, 'Главное меню', reply_markup=my_markups.main_menu)


@bot.callback_query_handler(func=lambda call: True)
def add_to_bin(call):
    if call.message:
        new_order = ''
        if call.data == 'none':
            bot.send_message(call.message.chat.id, 'Данный товар отсутствует на складе')
        elif call.data == 'uvedl_on':
            for u in dbhelp.User.select():
                if str(u.cid) == str(call.message.chat.id):
                    u.uvedl = '1'
                    u.save()
                    bot.send_message(call.message.chat.id, '✅Готово')
        elif call.data == 'uvedl_off':
            for u in dbhelp.User.select():
                if str(u.cid) == str(call.message.chat.id):
                    u.uvedl = '0'
                    u.save()
                    bot.send_message(call.message.chat.id, '✅Готово')
        else:
            for p in dbhelp.Product.select():
                if call.data == p.theme:
                    new_order = p.id
            for u in dbhelp.User.select():
                if str(u.cid) == str(call.message.chat.id):
                    if u.bin == 'none':
                        u.bin = str(new_order) + ' '
                        u.save()
                    else:
                        u.bin.split()
                        u.bin += str(new_order) + ' '
                        u.save()
            bot.send_message(call.message.chat.id, '🛍Товар добавлен в корзину')


@bot.message_handler(content_types=['text'])
def main(message):
    ccid = message.chat.id
    enter_name = 0
    enter_mes = 0
    for u in dbhelp.User.select():
        if str(u.cid) == str(ccid):
            if u.type == '1':
                enter_name = 1
            if u.sendmes == '1':
                enter_mes = 1
    if message.text == '❌Отмена':
        for u in dbhelp.User.select():
            if str(u.cid) == str(ccid):
                u.type = '0'
                u.save()
        bot.send_message(message.chat.id, 'Хорошо, вернемся к этому позже', reply_markup=my_markups.main_menu)
    if message.text == '❌Отменить':
        for u in dbhelp.User.select():
            if str(u.cid) == str(ccid):
                u.sendmes = '0'
                u.save()
        comtxt = open('commands.txt', encoding='utf-8')
        bot.send_message(message.chat.id, '📌Список команд:\n\n{}\n\nВыберите ниже раздел справки'.format(comtxt.read()), reply_markup=my_markups.help_page)
    elif enter_name == 1:
        for u in dbhelp.User.select():
            if str(u.cid) == str(ccid):
                u.name = message.text
                u.type = '2'
                bot.send_message(message.chat.id, 'Хорошо, {}, я запомнил😊'.format(u.name), reply_markup=my_markups.main_menu)
                u.save()
    elif enter_mes == 1:
        for u in dbhelp.User.select():
            if str(u.cid) == str(ccid):
                bot.send_message(680180012, '{}(@{} / @{}) оставил сообщение: \n{}'.format(u.name, message.from_user.username, message.chat.username, message.text))
                u.sendmes = '0'
                u.save()
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
        for u in dbhelp.User.select():
            if str(u.cid) == str(ccid):
                u.sendmes = '1'
                u.save()
    elif message.text == '👤Персональные данные':
        bot.send_message(message.chat.id, 'Персональные данные', reply_markup=my_markups.personal_page)
    elif message.text == '🔏Ввести имя':
        bot.send_message(message.chat.id, 'Я запомню введенное имя', reply_markup=my_markups.enter_page)
        for u in dbhelp.User.select():
            if str(u.cid) == str(ccid):
                u.type = '1'
                u.save()
    elif message.text == '🐻Мишки':
        bot.send_message(message.chat.id, 'По какому параметру сортировать медведей?', reply_markup=my_markups.sort_page)
    elif message.text == '📏По размеру':
        bot.send_message(message.chat.id, 'Выберите размер мишки', reply_markup=my_markups.medved_page)
    elif message.text == '🛒Выбрать товар':
        bot.send_message(message.chat.id, 'Выберите интересующий товар и нажмите на соответствующую кнопку😊', reply_markup=my_markups.menu_page)
    elif message.text == '🔮Разное':
        bot.send_message(message.chat.id, 'Извините, товаров этой категории нет в наличии😔', reply_markup=my_markups.no_goods_page)
    elif message.text == '🏷Имя':
        for u in dbhelp.User.select():
            if str(u.cid) == str(ccid):
                bot.send_message(message.chat.id, 'Текущее имя: {} \nИзменить?'.format(u.name), reply_markup=my_markups.start_page)
    elif message.text == '🛎Уведомления':
        a = ''
        mk1 = types.InlineKeyboardMarkup()
        mk2 = types.InlineKeyboardMarkup()
        for u in dbhelp.User.select():
            if str(u.cid) == str(ccid):
                if u.uvedl == '1':
                    mkb = types.InlineKeyboardButton(text='❌Выключить', callback_data='uvedl_off')
                    mk1.add(mkb)
                    bot.send_message(message.chat.id, 'Уведомления включены, выключить?', reply_markup=mk1)
                elif u.uvedl == '0':
                    mkb = types.InlineKeyboardButton(text='✅Включить', callback_data='uvedl_on')
                    mk2.add(mkb)
                    bot.send_message(message.chat.id, 'Уведомления выключены, включить?', reply_markup=mk2)
    elif message.text == '🛒Корзина':
        for u in dbhelp.User.select():
            if str(u.cid) == str(ccid):
                if u.bin == 'none':
                    bot.send_message(message.chat.id, '🛒Ваша корзина пуста', reply_markup=my_markups.bin_page)
                else:
                    u.bin.split(' ')
                    bot.send_message(message.chat.id, '🛒Товары в вашей корзине:')
                    for i in range(len(u.bin)):
                        for p in dbhelp.Product.select():
                            if str(u.bin[i]) == str(p.id):
                                bot.send_message(message.chat.id, '🐻{}, {} см., {} рублей'.format(p.name, p.size, p.price))
                                bot.send_photo(message.chat.id, open('teddybears/{}.jpg'.format(p.theme), 'rb'))
                    bot.send_message(message.chat.id, 'Оформить заказ?', reply_markup=my_markups.order_page)
    elif message.text == '🗑Очистить корзину':
        for u in dbhelp.User.select():
            if str(u.cid) == str(ccid):
                u.bin = 'none'
                u.save()
                bot.send_message(message.chat.id, '🗑Корзина очищена', reply_markup=my_markups.bin_page)
    elif message.text == '🎈Товары со скидкой':
        for p in dbhelp.Product.select():
            if p.type == '1' and p.sale != '0' and p.available != '0':
                bot.send_message(message.chat.id, '🐻{}, {} см., {} рублей с учетом скидки'.format(p.name, p.size, p.price))
                bot.send_photo(message.chat.id, open('teddybears/{}.jpg'.format(p.theme), 'rb'),
                               reply_markup=check_available(p.available, p.theme))
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
            if p.type == '2' and p.available != '0':
                bot.send_message(message.chat.id, '🎁{} {} см., {} рублей '.format(p.name, p.size, p.price))
                bot.send_photo(message.chat.id, open('teddybears/{}.jpg'.format(p.theme), 'rb'),
                               reply_markup=check_available(p.available, p.theme))
    else:
        comtxt = open('commands.txt', encoding='utf-8')
        bot.send_message(message.chat.id, '😟Не понимаю Вас, вот список команд:\n\n{}\n\n'.format(comtxt.read()), reply_markup=my_markups.go_to_main_menu)


def check_available(a, b):
    mkup1 = types.InlineKeyboardMarkup()
    mkup2 = types.InlineKeyboardMarkup()
    mkbt1 = types.InlineKeyboardButton(text='✅Добавить в корзину', callback_data=b)
    mkbt2 = types.InlineKeyboardButton(text='❌Нет в наличии', callback_data='none')
    mkup1.add(mkbt1)
    mkup2.add(mkbt2)
    if a == '1':
        return mkup1
    else:
        return mkup2


def show_product(product_type, size_type, message):
    for p in dbhelp.Product.select():
        if p.type == product_type and p.size_type == size_type and p.available != '0':
            bot.send_message(message.chat.id, '🐻{}, {} см., {} рублей'.format(p.name, p.size, p.price))
            bot.send_photo(message.chat.id, open('teddybears/{}.jpg'.format(p.theme), 'rb'),
                           reply_markup=check_available(p.available, p.theme))


@bot.message_handler(content_types=['sticker', 'pinned_message', 'photo', 'audio', 'document'])
def answer_not_a_text(message):
    comtxt = open('commands.txt', encoding='utf-8')
    bot.send_message(message.chat.id, '😟Не могу никак на это ответить, вот список команд\n\n{}\n\n'.format(comtxt.read()), reply_markup=my_markups.go_to_main_menu)


if __name__ == '__main__':
    bot.polling(none_stop=True)
