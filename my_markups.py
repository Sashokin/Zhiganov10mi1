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