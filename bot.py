# -*- coding: utf-8 -*-
import telebot
from telebot import types
import my_markups
import config_for_token
import dbhelp
# todo: исправить тотал, доставка, залить на сервер, имя, первая настройка, faq

bot = telebot.TeleBot(config_for_token.token)  # токен спрятан, тк мой репозиторий на гитхабе публичный


# db = SqliteDatabase('database.db')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    ccid = message.chat.id
    cb = 0
    for u in dbhelp.User.select():  # Проверяем, есть ли пользователь в базе данных
        if str(u.cid) == str(ccid):
            cb = 1
    if cb == 0:  # Добавляем его
        ccid = dbhelp.User(cid=ccid, type='0', name='none', phone='none', uvedl='1', orders='', sendmes='0', bin='none', total='0', kolvo='0', tov='', doppredl='0', last_total='', product_show='0')
        ccid.save()
        bot.send_message(message.chat.id, 'Привет![😊](https://i.imgur.com/mPMdr9B.jpg)'
                                          ' Я бот магазина metoyou!', parse_mode='markdown', reply_markup=my_markups.main_menu)
    else:  # Или же приветствуем
        for u in dbhelp.User.select():
            if str(u.cid) == str(ccid):
                if u.name == 'none':
                    bot.send_message(message.chat.id, 'Привет, рад видеть снова!😊', reply_markup=my_markups.main_menu)
                else:
                    bot.send_message(message.chat.id, 'Привет, {} 😊'.format(u.name), reply_markup=my_markups.main_menu)


@bot.message_handler(commands=['help'])  # Список команд + страница помощи
def send_help(message):
    comtxt = open('commands.txt', encoding='utf-8')
    bot.send_message(message.chat.id, '📌Список команд:\n\n{}\n\nВыберите ниже раздел справки'.format(comtxt.read()), reply_markup=my_markups.help_page)


@bot.message_handler(commands=['main'])  # Главное меню
def main_menu(message):
    bot.send_message(message.chat.id, 'Главное меню', reply_markup=my_markups.main_menu)


@bot.message_handler(commands=['buy'])  # Вкладка покупки
def buy_com(message):
    bot.send_message(message.chat.id, 'Выберите интересующий товар и нажмите на соответствующую кнопку😊', reply_markup=my_markups.menu_page)


@bot.message_handler(commands=['bin'])  # Вкладка корзины
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
                            bot.send_message(message.chat.id, '[🐻]({}){}, {} см., {} рублей'.format(p.link, p.name, p.size, p.price), parse_mode='markdown', reply_markup=mark)
                bot.send_message(message.chat.id, 'Общая сумма: {} рублей \nОформить заказ?'.format(u.total),reply_markup=my_markups.order_page)


@bot.message_handler(commands=['personal'])  # Вкладка данных о пользователе
def personal_com(message):
    bot.send_message(message.chat.id, 'Персональные данные', reply_markup=my_markups.personal_page)


@bot.callback_query_handler(func=lambda call: True)  # Обработчик callback кнопок
def add_to_bin(call):
    if call.message:
        new_order = ''
        new_total = 0
        kolvo = 0
        del_order = ''
        mk = types.InlineKeyboardMarkup()
        if call.data == 'none':  # Клик по товару, которого нет на складе
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text='❌Данный товар отсутствует на складе')
        elif call.data == 'uvedl_on':  # Включение уведомлений
            for u in dbhelp.User.select():
                if str(u.cid) == str(call.message.chat.id):
                    u.uvedl = '1'
                    u.save()
                    mkb = types.InlineKeyboardButton(text='❌Выключить', callback_data='uvedl_off')
                    mk.add(mkb)
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Уведомления включены, выключить?', reply_markup=mk)
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text='✅Готово')
        elif call.data == 'uvedl_off':  # Выключение уведомлений
            for u in dbhelp.User.select():
                if str(u.cid) == str(call.message.chat.id):
                    u.uvedl = '0'
                    u.save()
                    mkb = types.InlineKeyboardButton(text='✅Включить', callback_data='uvedl_on')
                    mk.add(mkb)
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Уведомления выключены, включить?', reply_markup=mk)
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text='✅Готово')
        elif call.data == 'pr_show_on':  # Включить показ только имеющихся товаров
            for u in dbhelp.User.select():
                if str(u.cid) == str(call.message.chat.id):
                    u.product_show = '1'
                    u.save()
                    mkb = types.InlineKeyboardButton(text='🛍Показывать все', callback_data='pr_show_off')
                    mk.add(mkb)
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Показываются только товары в наличии. Предлагать все товары?', reply_markup=mk)
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text='✅Готово')
        elif call.data == 'pr_show_off':  # Показывать все товары
            for u in dbhelp.User.select():
                if str(u.cid) == str(call.message.chat.id):
                    u.product_show = '0'
                    u.save()
                    mkb = types.InlineKeyboardButton(text='🛍Показывать только в наличии', callback_data='pr_show_on')
                    mk.add(mkb)
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Показываются все товары. Предлагать только товары в наличии?', reply_markup=mk)
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text='✅Готово')
        elif call.data[:4] == 'del_':  # Удаление из корзины
            for p in dbhelp.Product.select():
                if int(call.data[4:]) == int(p.id):
                    del_order = p.id
                    new_total = int(p.price)
            for u in dbhelp.User.select():
                if str(u.cid) == str(call.message.chat.id):
                    new_bin = u.bin
                    new_bin = new_bin.split(str(del_order))[0] + str(del_order).join(new_bin.split(str(del_order))[1:])
                    u.bin = new_bin
                    a = int(u.total)
                    new_total = a-new_total
                    kolvo = int(u.kolvo)
                    kolvo -= 1
                    u.total = str(new_total)
                    u.kolvo = str(kolvo)
                    u.save()
                    hggh = 'rep_'+call.data[4:]
                    mkb = types.InlineKeyboardButton(text='✅Восстановить товар', callback_data=hggh)
                    mk.add(mkb)
                    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=mk)
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text='🛍Товар удален из корзины')
                    for i in range(10):
                        if u.bin == ' '*i:
                            u.bin = 'none'
                            u.save()
        elif call.data[:4] == 'rep_':  # Восстановление товара
            for p in dbhelp.Product.select():
                if int(call.data[4:]) == int(p.id):
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
            hggh = 'del_' + call.data[4:]
            mkb = types.InlineKeyboardButton(text='❌Удалить товар', callback_data=hggh)
            mk.add(mkb)
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=mk)
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text='🛍Товар восстановлен')
        elif call.data == 'go_to_bin':
            for u in dbhelp.User.select():
                if str(u.cid) == str(call.message.chat.id):
                    if u.bin == 'none':
                        bot.send_message(call.message.chat.id, '🛒Ваша корзина пуста', reply_markup=my_markups.bin_page)
                    else:
                        bot.send_message(call.message.chat.id, '🛒Товары в вашей корзине:')
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
                                    bot.send_message(call.message.chat.id,
                                                     '[🐻]({}){}, {} см., {} рублей'.format(p.link, p.name, p.size, p.price), parse_mode='markdown', reply_markup=mark)
                        bot.send_message(call.message.chat.id, 'Общая сумма: {} рублей \nОформить заказ?'.format(u.total), reply_markup=my_markups.order_page)
        else:  # Добавление в корзину
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
                    mkb = types.InlineKeyboardButton(text='✅Добавить в корзину', callback_data=call.data)
                    mkdk = types.InlineKeyboardButton(text='🛒Перейти в корзину ({})'.format(u.kolvo), callback_data='go_to_bin')
                    mk.add(mkb)
                    mk.add(mkdk)
                    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=mk)
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text='🛍Товар добавлен в корзину')


@bot.message_handler(content_types=['contact'])  # Отправление контакта при оформлении заказа
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
                abfc = int(u.kolvo) % 10
                if abfc == 0 or abfc == 5 or abfc == 6 or abfc == 7 or abfc == 8 or abfc == 9:
                    u.tov = 'товаров'
                elif abfc == 1:
                    u.tov = 'товар'
                elif abfc == 2 or abfc == 3 or abfc == 4:
                    u.tov = 'товара'
                bot.send_message(message.chat.id, '✅Проверьте и подтвердите заказ:\nСумма к оплате: {} рублей + доставка 300 рублей.\n{} {}.\nОплата наличными при получении.\nМенеджер свяжется с Вами по этому номеру({}) для уточнения времени и места доставки.'.format(u.total, u.kolvo, u.tov, u.phone), reply_markup=my_markups.confirm_page)


@bot.message_handler(content_types=['text'])  # Основной обработчик, принимает текст
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
        send_help(message)
    elif message.text == '🥇Качество продукции':
        bot.send_message(message.chat.id, '👍Мы занимаемся продажей оригинальной продукции английской компании Carte Blanche Greetings LTD \nВся продукция прошла предпродажную подготовку и торговую сертификацию\n\n [Как отличить подделку от оригинала](https://market.yandex.ru/journal/expertise/kak-otlichit-originalnogo-mishku-Me-to-You-ot-poddelki)', parse_mode='markdown')
    elif message.text == '⌨️Задать вопрос':
        bot.send_message(message.chat.id, 'Напишите свое сообщение, оно сразу будет передано нам', reply_markup=my_markups.enter_page2)
        for u in dbhelp.User.select():
            if str(u.cid) == str(ccid):
                u.sendmes = '1'
                u.save()
    elif message.text == '👤Пользовательские настройки':
        personal_com(message)
    elif message.text == '⚙️Настройка показа':
        mk1 = types.InlineKeyboardMarkup()
        mk2 = types.InlineKeyboardMarkup()
        for u in dbhelp.User.select():
            if str(u.cid) == str(ccid):
                if u.product_show == '1':
                    mkb = types.InlineKeyboardButton(text='🛍Показывать все', callback_data='pr_show_off')
                    mk1.add(mkb)
                    bot.send_message(message.chat.id, 'Показываются только товары в наличии. Предлагать все товары?', reply_markup=mk1)
                elif u.product_show == '0':
                    mkb = types.InlineKeyboardButton(text='🛍Показывать только в наличии', callback_data='pr_show_on')
                    mk2.add(mkb)
                    bot.send_message(message.chat.id, 'Показываются все товары. Предлагать только товары в наличии?', reply_markup=mk2)
    elif message.text == '🔏Ввести имя':
        bot.send_message(message.chat.id, 'Я запомню введенное имя', reply_markup=my_markups.enter_page)
        for u in dbhelp.User.select():
            if str(u.cid) == str(ccid):
                u.type = '1'
                u.save()
    elif message.text == '🐻Мишки' or message.text == 'Мишки':
        bot.send_message(message.chat.id, 'Выберите размер мишки', reply_markup=my_markups.medved_page)
    elif message.text == '🛒Выбрать товар':
        bot.send_message(message.chat.id, 'Выберите интересующий товар😊', reply_markup=my_markups.menu_page)
    elif message.text == '🔮Разное':
        bot.send_message(message.chat.id, 'Извините, товаров этой категории нет в наличии😔')
    elif message.text == '🏷Имя':
        for u in dbhelp.User.select():
            if str(u.cid) == str(ccid):
                bot.send_message(message.chat.id, 'Текущее имя: {} \nИзменить?'.format(u.name), reply_markup=my_markups.start_page)
    elif message.text == '🛎Уведомления':
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
    elif message.text == '🛒Корзина' or message.text == 'Корзина':
        bin_com(message)
    elif message.text == '🗑Очистить корзину':
        for u in dbhelp.User.select():
            if str(u.cid) == str(ccid):
                u.bin = 'none'
                u.total = '0'
                u.kolvo = '0'
                u.save()
                bot.send_message(message.chat.id, '🗑Корзина очищена', reply_markup=my_markups.bin_page)
    elif message.text == '🎈Товары со скидкой' or message.text == 'Скидка':
        smth_sended = 0
        for p in dbhelp.Product.select():
            if p.type == '1' and p.sale != '0' and p.available != '0':
                bot.send_message(message.chat.id, '[🐻]({}){}, {} см., {} рублей с учетом скидки'.format(p.link, p.name, p.size, p.price), parse_mode='markdown', reply_markup=check_available(p.available, p.theme))
                smth_sended = 1
        if smth_sended == 0:
            bot.send_message(message.chat.id, 'Извините, товаров этой категории нет в наличии😔')
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
    elif message.text == '🎁Подарочные упаковки' or message.text == '✅Посмотреть':
        product_show_set = 0
        for u in dbhelp.User.select():
            if str(u.cid) == str(message.chat.id):
                if u.product_show == '1':
                    product_show_set = 1
        for p in dbhelp.Product.select():
            if product_show_set == 1:
                if p.type == '2' and p.available != '0':
                    bot.send_message(message.chat.id, '[🎁]({}){} {} см., {} рублей '.format(p.link, p.name, p.size, p.price), parse_mode='markdown', reply_markup=check_available(p.available, p.theme))
            else:
                if p.type == '2':
                    bot.send_message(message.chat.id, '[🎁]({}){} {} см., {} рублей '.format(p.link, p.name, p.size, p.price), parse_mode='markdown', reply_markup=check_available(p.available, p.theme))

    elif message.text == '📦Заказы' or message.text == 'Заказы':
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
                                    statusf = '❕Подтвержден, будет доставлен в назначенное время({})'.format(o.time)
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
                u.doppredl = check_dop_predl(ccid)
                if u.doppredl == '1':
                    bot.send_message(message.chat.id, '📦{} {} на {} рублей\nДоставка будет стоить 300 рублей\nОтправьте номер телефон, менеджер свяжется с Вами для согласования места, даты и времени доставки'.format(u.kolvo, u.tov, u.total), reply_markup=my_markups.phone_page)
                else:
                    bot.send_message(message.chat.id, '✌️Я изучил заказ и пришел к выводу, что в него идеально впишутся некоторые товары', reply_markup=my_markups.dop_predl_page)
                u.sendmes = '2'
                u.save()
    elif message.text == '🗳Перейти к оформлению заказа':
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
                fccid = dbhelp.Order.create(id=fs, user=str(ccid), phone=u.phone, bin=u.bin, total=str(int(u.total)+300), status='0', time='')
                fccid.save()
                bot.send_message(680180012, 'Новый заказ:\nСумма: {}, товары: {}, телефон: {}'.format(str(int(u.total)+300), u.bin, u.phone), reply_markup=my_markups.main_menu)
                u.bin = 'none'
                u.total = '0'
                u.kolvo = '0'
                u.orders = str(u.orders) + str('{} '.format(fs))
                u.save()
                bot.send_message(message.chat.id, '✅Заказ передан менеджеру, спасибо за покупку', reply_markup=my_markups.main_menu)
    elif message.text == 'Привет':
        bot.send_message(message.chat.id, '✌️Привет')
    else:
        comtxt = open('commands.txt', encoding='utf-8')
        bot.send_message(message.chat.id, '😟Не понимаю Вас, вот список команд:\n\n{}\n\n'.format(comtxt.read()), reply_markup=my_markups.go_to_main_menu)


def check_available(a, b):  # Проверка на наличие товара
    mkup1 = types.InlineKeyboardMarkup()
    mkup2 = types.InlineKeyboardMarkup()
    mkbt1 = types.InlineKeyboardButton(text='✅Добавить в корзину', callback_data=b)
    mkbt2 = types.InlineKeyboardButton(text='❌Нет в наличии', callback_data='none')
    mkup1.add(mkbt1)
    mkup2.add(mkbt2)
    if a != '0':
        return mkup1
    else:
        return mkup2


def show_product(product_type, size_type, message):  # Вывод товара
    product_show_set = 0
    for u in dbhelp.User.select():
        if str(u.cid) == str(message.chat.id):
            if u.product_show == '1':
                product_show_set = 1
    for p in dbhelp.Product.select():
        if product_show_set == 1:
            if p.type == product_type and p.size_type == size_type and p.available != '0':
                bot.send_message(message.chat.id, '[🐻]({}){}, {} см., {} рублей'.format(p.link, p.name, p.size, p.price), parse_mode='markdown', reply_markup=check_available(p.available, p.theme))
        else:
            if p.type == product_type and p.size_type == size_type:
                bot.send_message(message.chat.id, '[🐻]({}){}, {} см., {} рублей'.format(p.link, p.name, p.size, p.price), parse_mode='markdown', reply_markup=check_available(p.available, p.theme))


def check_dop_predl(ccid):  # Проверяем, нужен ли пользователю какой-либо дополнительный товар
    for u in dbhelp.User.select():
        if str(u.cid) == str(ccid):
            u.bin = u.bin.split()
            n = len(u.bin)
            for i in range(n):
                u.bin[i] = int(u.bin[i])
            psps = 0
            for i in range(n):
                for p in dbhelp.Product.select():
                    if str(u.bin[i]) == str(p.id) and p.type == '2':
                        psps = 1
            if psps == 1:
                return '1'
            else:
                return '0'


@bot.message_handler(content_types=['sticker', 'pinned_message', 'photo', 'audio', 'document'])  # Обработчик ненужных типов контента
def answer_not_a_text(message):
    comtxt = open('commands.txt', encoding='utf-8')
    bot.send_message(message.chat.id, '😟Не могу никак на это ответить, вот список команд\n\n{}\n\n'.format(comtxt.read()), reply_markup=my_markups.go_to_main_menu)


if __name__ == '__main__':
    bot.polling(none_stop=True)
