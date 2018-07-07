# -*- coding: utf-8 -*-
import config
import telebot
import time
from telebot import types


to_site = types.InlineKeyboardMarkup()
btn_to_site = types.InlineKeyboardButton(text="Перейти на сайт", url="www.metoyou-shop.ru")
to_site.add(btn_to_site)

go_to_main_menu = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
btn_main_menu = types.KeyboardButton('Главное меню')
go_to_main_menu.add(btn_main_menu)

main_menu = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
btn_person_data = types.KeyboardButton('Персональные данные')
btn_help = types.KeyboardButton('Помощь и связь')
main_menu.add(btn_person_data, btn_help)

help_page = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
btn_phone_us = types.KeyboardButton('Позвонить')
btn_mail_us = types.KeyboardButton('Написать')
btn_info = types.KeyboardButton('Информация на сайте')
btn_back_main_menu = types.KeyboardButton('Вернуться в главное меню')
help_page.row(btn_phone_us, btn_mail_us)
help_page.add(btn_info, btn_back_main_menu)

help_page_out_site = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
help_page_out_site.row(btn_phone_us, btn_mail_us)
help_page_out_site.add(btn_back_main_menu)

personal_page = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
btn_name = types.KeyboardButton('Имя')
btn_phone = types.KeyboardButton('Телефон')
btn_adress = types.KeyboardButton('Адрес')
btn_news = types.KeyboardButton('Уведомления')
btn_orders = types.KeyboardButton('Заказы')
personal_page.row(btn_name, btn_phone, btn_adress)
personal_page.add(btn_news, btn_orders, btn_back_main_menu)
