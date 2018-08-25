# -*- coding: utf-8 -*-
import config
import telebot
from telebot import types
import my_markups
import config_for_token
from peewee import *


#c.execute('''CREATE TABLE goods (type real, name text, theme text, size_type real, price real, available real, sale real)''')
#type - 1 - мишка, 2 - упаковка, 3 другое. Name - имя. Theme - артикул. Size_type - размер(если мишка), 1 - 10-18, 2 - 20, 3 - 23-25, 4 - 30, 5 - 40-50, 6 - 60. size - размер. Price - цена. Available - доступность, 0/1. Sale - есть ли скидка на товар, 0-нет, 1-100 - размер скидки.

db = SqliteDatabase('database.db')


class Product(Model):
    type = CharField()
    name = CharField()
    theme = CharField()
    size_type = CharField()
    size = CharField()
    price = CharField()
    available = CharField()
    sale = CharField()

    class Meta:
        database = db


class User(Model):
    cid = CharField() #id юзера
    type = CharField() #изначально=0, 1 - вводит имя, 2 - ввел имя
    name = CharField() #имя пользователя
    phone = CharField() #телефон пользователя
    uvedl = CharField() #вкл/выкл новости, новые товары и тд, изначально = 1
    orders = CharField() #активные заказы

    class Meta:
        database = db


db.connect()
#db.create_tables([Product, User])


#G01W3807 = Product(type=1, name='Медвежонок Tatty Teddy в майке с сердечком', theme='G01W3807', size_type=1, size=10, price=600, available=1, sale=0)
#G01W3807.save()
#user = User(cid=cid, type ='0, name='none', phone='none', uvedl='1', orders='none')