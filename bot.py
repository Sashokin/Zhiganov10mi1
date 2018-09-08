# -*- coding: utf-8 -*-
import telebot
from telebot import types
import my_markups
import config_for_token
from peewee import *
import dbhelp
import time
#todo: сортировка медведей по тематике, проверить наличие+кол-во, доп предложения, убрать все ссылки на сайт, отслеживание заказов(доделать), ввести имя - встроенная кнопка

bot = telebot.TeleBot(config_for_token.token) #токен спрятан, тк мой репозиторий на гитхабе публичный


#db = SqliteDatabase('database.db')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    ccid = message.chat.id
    cb = 0
    for u in dbhelp.User.select():
        if str(u.cid) == str(ccid):
            cb = 1
    if cb == 0:
        ccid = dbhelp.User(cid=ccid, type='0', name='none', phone='none', uvedl='1', orders='', sendmes='0', bin='none', total='0', kolvo='0', tov='')
        ccid.save()
        bot.send_message(message.chat.id, 'Привет![😊](https://i.imgur.com/mPMdr9B.jpg)'
                                          ' Я бот магазина metoyou! А тебя я еще не знаю😔', parse_mode='markdown', reply_markup=my_markups.start_page)
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


@bot.message_handler(commands=['buy'])
def buy_com(message):
    bot.send_message(message.chat.id, 'Выберите интересующий товар и нажмите на соответствующую кнопку😊', reply_markup=my_markups.menu_page)


@bot.message_handler(commands=['bin'])
def bin_com(message):
    ccid = message.chat.id
    for u in dbhelp.User.select():
        if str(u.cid) == str(ccid):
            if u.bin == 'none':
                bot.send_message(message.chat.id, '🛒Ваша корзина пуста', reply_markup=my_markups.bin_page)
            else:
                bot.send_message(message.chat.id, '🛒Товары в вашей корзине:')
                u.bin = u.bin.split()
                n = len(u.bin)
                for i in range(n):
                    u.bin[i] = int(u.bin[i])
                for i in range(n):
                    for p in dbhelp.Product.select():
                        mark = types.InlineKeyboardMarkup()
                        mkbtt = types.InlineKeyboardButton(text='❌Удалить товар', callback_data='del_{}'.format(p.id))
                        mark.add(mkbtt)
                        if str(u.bin[i]) == str(p.id):
                            bot.send_message(message.chat.id,
                                             '[🐻]({}){}, {} см., {} рублей'.format(p.link, p.name, p.size, p.price),
                                             parse_mode='markdown', reply_markup=mark)
                bot.send_message(message.chat.id, 'Общая сумма: {} рублей \nОформить заказ?'.format(u.total),
                                 reply_markup=my_markups.order_page)


@bot.message_handler(commands=['personal'])
def personal_com(message):
    bot.send_message(message.chat.id, 'Персональные данные', reply_markup=my_markups.personal_page)


@bot.callback_query_handler(func=lambda call: True)
def add_to_bin(call):
    if call.message:
        new_order = ''
        new_total = 0
        kolvo = 0
        del_order = ''
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
        elif call.data[:4] == 'del_':
            for p in dbhelp.Product.select():
                if int(call.data[4:]) == int(p.id):
                    del_order = p.id
                    new_total = int(p.price)
            for u in dbhelp.User.select():
                if str(u.cid) == str(call.message.chat.id):
                    new_bin = u.bin
                    new_bin = new_bin.split(str(del_order))[0] + str(del_order).join(new_bin.split(str(del_order))[1:])
                    if u.bin == new_bin:
                        bot.send_message(call.message.chat.id, '🛍Этого товара уже нет в корзине')
                    else:
                        u.bin = new_bin
                        a = int(u.total)
                        new_total = a-new_total
                        kolvo = int(u.kolvo)
                        kolvo -= 1
                        u.total = str(new_total)
                        u.kolvo = str(kolvo)
                        u.save()
                        bot.send_message(call.message.chat.id, '🛍Товар удален из корзины')
                    for i in range(10):
                        if u.bin == ' '*i:
                            u.bin = 'none'
                            u.save()
        else:
            for p in dbhelp.Product.select():
                if call.data == p.theme:
                    new_order = p.id
                    new_total = int(p.price)
            for u in dbhelp.User.select():
                if str(u.cid) == str(call.message.chat.id):
                    if u.bin == 'none':
                        u.bin = str(new_order) + ' '
                        a = int(u.total)
                        new_total +=a
                        u.total = str(new_total)
                        kolvo = int(u.kolvo)
                        kolvo += 1
                        u.kolvo = str(kolvo)
                        u.save()
                    else:
                        u.bin += str(new_order) + ' '
                        a = int(u.total)
                        new_total += a
                        u.total = str(new_total)
                        u.total = str(new_total)
                        kolvo = int(u.kolvo)
                        kolvo += 1
                        u.kolvo = str(kolvo)
                        u.save()
            bot.send_message(call.message.chat.id, '🛍Товар добавлен в корзину')


@bot.message_handler(content_types=['contact'])
def main1(message):
    ccid = message.chat.id
    enter_phone = 0
    for u in dbhelp.User.select():
        if str(u.cid) == str(ccid):
            if u.sendmes == '2':
                enter_phone = 1
    if enter_phone == 1:
        for u in dbhelp.User.select():
            if str(u.cid) == str(ccid):
                u.phone = message.contact.phone_number
                u.sendmes = '0'
                u.save()
                abfc = int(u.kolvo)%10
                if abfc == 0 or abfc == 5 or abfc == 6 or abfc == 7 or abfc == 8 or abfc == 9:
                    u.tov = 'товаров'
                elif abfc == 1:
                    u.tov = 'товар'
                elif abfc == 2 or abfc == 3 or abfc == 4:
                    u.tov = 'товара'
                bot.send_message(message.chat.id, '✅Проверьте и подтвердите заказ:\nСумма к оплате: {} рублей + доставка 300 рублей.\n{} {}.\nОплата наличными при получении.\nМенеджер свяжется с Вами по этому номеру({}) для уточнения времени и места доставки.'.format(u.total, u.kolvo, u.tov, u.phone), reply_markup=my_markups.confirm_page)


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
    elif message.text == '❌Отменить':
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
                    bot.send_message(message.chat.id, '🛒Товары в вашей корзине:')
                    u.bin = u.bin.split()
                    n = len(u.bin)
                    for i in range(n):
                        u.bin[i] = int(u.bin[i])
                    for i in range(n):
                        for p in dbhelp.Product.select():
                            mark = types.InlineKeyboardMarkup()
                            mkbtt = types.InlineKeyboardButton(text='❌Удалить товар', callback_data='del_{}'.format(p.id))
                            mark.add(mkbtt)
                            if str(u.bin[i]) == str(p.id):
                                bot.send_message(message.chat.id, '[🐻]({}){}, {} см., {} рублей'.format(p.link, p.name, p.size, p.price), parse_mode='markdown', reply_markup=mark)
                    bot.send_message(message.chat.id, 'Общая сумма: {} рублей \nОформить заказ?'.format(u.total), reply_markup=my_markups.order_page)
    elif message.text == '🗑Очистить корзину':
        for u in dbhelp.User.select():
            if str(u.cid) == str(ccid):
                u.bin = 'none'
                u.total = '0'
                u.save()
                bot.send_message(message.chat.id, '🗑Корзина очищена', reply_markup=my_markups.bin_page)
    elif message.text == '🎈Товары со скидкой':
        for p in dbhelp.Product.select():
            if p.type == '1' and p.sale != '0' and p.available != '0':
                bot.send_message(message.chat.id, '[🐻]({}){}, {} см., {} рублей с учетом скидки'.format(p.link, p.name, p.size, p.price), parse_mode='markdown', reply_markup=check_available(p.available, p.theme))
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
                bot.send_message(message.chat.id, '[🎁]({}){} {} см., {} рублей '.format(p.link, p.name, p.size, p.price), parse_mode='markdown', reply_markup=check_available(p.available, p.theme))
    elif message.text == '📦Заказы':
        for u in dbhelp.User.select():
            if str(u.cid) == str(ccid):
                u.orders = u.orders.split()
                n = len(u.orders)
                for i in range(n):
                    u.orders[i] = int(u.orders[i])
                for i in range(n):
                    for o in dbhelp.Order.select():
                        if str(u.orders[i]) == str(o.id):
                                o.bin = o.bin.split()
                                s = len(o.bin)
                                for abc in range(s):
                                    o.bin[abc] = int(o.bin[abc])
                                for abcd in range(s):
                                    for p in dbhelp.Product.select():
                                        if str(o.bin[abcd]) == str(p.id):
                                            bot.send_message(message.chat.id, '[🐻]({}){}, {} см., {} рублей'.format(p.link, p.name, p.size, p.price), parse_mode='markdown')
                                statusf = ''
                                if o.status == '0':
                                    statusf = '⚠️Не подтвержден'
                                elif o.status == '1':
                                    statusf = '❕Подтвержден, будет доставлен в обговоренное время'
                                elif o.status == '2':
                                    statusf = '✅Получен'
                                elif o.status == '3':
                                    statusf = '⛔️Отменен'
                                bot.send_message(message.chat.id, 'Общая сумма заказа: {} рублей\nСтатус заказа: {}'.format(o.total, statusf))
    elif message.text == '🗳Оформить заказ':
        for u in dbhelp.User.select():
            if str(u.cid) == str(ccid):
                abfc = int(u.kolvo) % 10
                if abfc == 0 or abfc == 5 or abfc == 6 or abfc == 7 or abfc == 8 or abfc == 9:
                    u.tov = 'товаров'
                elif abfc == 1:
                    u.tov = 'товар'
                elif abfc == 2 or abfc == 3 or abfc == 4:
                    u.tov = 'товара'
                bot.send_message(message.chat.id, '📦{} {} на {} рублей\nДоставка будет стоить 300 рублей\nОставьте номер телефон, менеджер свяжется с Вами для согласования места, даты и времени доставки'.format(u.kolvo, u.tov, u.total), reply_markup=my_markups.phone_page)
                u.sendmes = '2'
                u.save()
    elif message.text == '✅Подтвердить':
        for u in dbhelp.User.select():
            if str(u.cid) == str(ccid):
                fs = 0
                for i in dbhelp.Order.select():
                    fs += 1
                fccid = ''
                fccid = str(ccid)+str(fs)
                fccid = dbhelp.Order.create(id=fs, user=str(ccid), phone=u.phone, bin=u.bin, total=str(int(u.total)+300), status='0')
                fccid.save()
                bot.send_message(680180012, 'Новый заказ:\nСумма: {}, товары: {}, телефон: {}'.format(str(int(u.total)+300), u.bin, u.phone), reply_markup=my_markups.main_menu)
                u.bin = 'none'
                u.total = '0'
                u.kolvo = '0'
                u.orders = str(u.orders) + str('{} '.format(fs))
                u.save()
                fs = 0
                f = ''
                bot.send_message(message.chat.id, '✅Заказ передан менеджеру, спасибо за покупку', reply_markup=my_markups.main_menu)
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
        if p.type == product_type and p.size_type == size_type:
            bot.send_message(message.chat.id, '[🐻]({}){}, {} см., {} рублей'.format(p.link, p.name, p.size, p.price), parse_mode='markdown', reply_markup=check_available(p.available, p.theme))


@bot.message_handler(content_types=['sticker', 'pinned_message', 'photo', 'audio', 'document'])
def answer_not_a_text(message):
    comtxt = open('commands.txt', encoding='utf-8')
    bot.send_message(message.chat.id, '😟Не могу никак на это ответить, вот список команд\n\n{}\n\n'.format(comtxt.read()), reply_markup=my_markups.go_to_main_menu)


if __name__ == '__main__':
    bot.polling(none_stop=True)
