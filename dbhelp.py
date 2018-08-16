# -*- coding: utf-8 -*-
import config
import telebot
from telebot import types
import my_markups
import config_for_token


#c.execute('''CREATE TABLE goods (type real, name text, theme text, size_type real, price real, available real, photo text, sale real)''')
#type - 1 - мишка, 2 - упаковка, 3 другое. Name - имя. Theme - артикул. Size_type - размер(если мишка), 1 - 7-18, 2 - 20-23, 3 - 25, 4 - 30, 5 - 40-50, 6 - 60. Price - цена. Available - доступность, 0/1. Photo - путь к изображению. Sale - есть ли скидка на товар, 0-нет, 1-100 - размер скидки.
