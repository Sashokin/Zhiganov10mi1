# -*- coding: utf-8 -*-
import config
import telebot
import time
from telebot import types
import bot


to_site = types.InlineKeyboardMarkup()
btn_to_site = types.InlineKeyboardButton(text="Перейти на сайт", url="www.metoyou-shop.ru")
to_site.add(btn_to_site)

go_to_main_menu = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
btn_main_menu = types.KeyboardButton('🚪Главное меню')
go_to_main_menu.add(btn_main_menu)

main_menu = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
btn_choose = types.KeyboardButton('🛒Выбрать товар')
btn_bin = types.KeyboardButton('🛍Корзина')
btn_person_data = types.KeyboardButton('👤Персональные данные')
btn_help = types.KeyboardButton('❓Помощь и связь')
main_menu.row(btn_choose, btn_bin)
main_menu.row(btn_person_data, btn_help)

help_page = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
btn_phone_us = types.KeyboardButton('📞Позвонить')
btn_mail_us = types.KeyboardButton('⌨️Написать')
btn_info = types.KeyboardButton('📋Информация на сайте')
btn_back_main_menu = types.KeyboardButton('🚪Вернуться в главное меню')
help_page.row(btn_phone_us, btn_mail_us)
help_page.add(btn_info, btn_back_main_menu)

help_page_out_site = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
help_page_out_site.row(btn_phone_us, btn_mail_us)
help_page_out_site.add(btn_back_main_menu)

personal_page = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
btn_name = types.KeyboardButton('Имя')
btn_news = types.KeyboardButton('🛎Уведомления')
#btn_change_personal = types.KeyboardButton('🔏Изменить персональные данные')
btn_orders = types.KeyboardButton('📦Заказы')
personal_page.row(btn_name, btn_news, btn_orders)
personal_page.add(btn_back_main_menu)

geophone_page = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
btn_phone = types.KeyboardButton(text='Отправить номер телефона', request_contact=True)
btn_geo = types.KeyboardButton(text='Отправить местоположение', request_location=True)
geophone_page.add(btn_phone, btn_geo, btn_back_main_menu)

medved_page = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
btn_718 = types.KeyboardButton('🐻10-18 сантиметров🐻')
btn_2023 = types.KeyboardButton('🐻20 сантиметров🐻')
btn_25 = types.KeyboardButton('🐻23-25 сантиметров🐻')
btn_30 = types.KeyboardButton('🐻30 сантиметров🐻')
btn_4050 = types.KeyboardButton('🐻40-50 сантиметров🐻')
#btn_60 = types.KeyboardButton('🐻60 и больше🐻')
medved_page.add(btn_718, btn_2023, btn_25, btn_30, btn_4050, btn_back_main_menu)

menu_page = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
btn_sales = types.KeyboardButton('🎈Товары со скидкой')
btn_medvedi = types.KeyboardButton('🐻Мишки')
#btn_posuda = types.KeyboardButton('🍴Посуда🍴')
btn_paket = types.KeyboardButton('🎁Подарочные упаковки')
btn_raznoe = types.KeyboardButton('🔮Разное')
menu_page.row(btn_medvedi, btn_sales)
menu_page.row(btn_paket, btn_raznoe)
menu_page.add(btn_back_main_menu)

sort_page = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
btn_size = types.KeyboardButton('📏По размеру')
btn_theme = types.KeyboardButton('🎉По тематике')
sort_page.row(btn_size, btn_theme)
sort_page.add(btn_back_main_menu)

no_goods_page = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
no_goods_page.add(btn_choose, btn_main_menu)

start_page = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
btn_input_name = types.KeyboardButton('🔏Ввести имя')
start_page.add(btn_input_name, btn_main_menu)

enter_page = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
btn_otmena = types.KeyboardButton('❌Отмена')
enter_page.add(btn_otmena)

enter_page2 = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
btn_otmena2 = types.KeyboardButton('❌Отменить')
enter_page2.add(btn_otmena2)