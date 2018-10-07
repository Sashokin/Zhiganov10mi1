# -*- coding: utf-8 -*-
from peewee import *


db = SqliteDatabase('database.db')


class Product(Model):
    type = CharField()  # Тип продукта: 1 - мишка, 2 - упаковка, 3 другое.
    name = CharField()  # Название
    theme = CharField()  # Артикул
    size_type = CharField()  # Размер(если мишка), 1 - 10-18, 2 - 20, 3 - 23-25, 4 - 30, 5 - 40-50, 6 - 60
    size = CharField()  # Точный размер в см
    price = CharField()  # Цена
    available = CharField()  # Доступность
    sale = CharField()  # Размер скидки
    link = CharField()  # Ссылка на картинку

    class Meta:
        database = db


class User(Model):
    cid = CharField()  # id юзера
    type = CharField()  # изначально=0, 1 - вводит имя, 2 - ввел имя
    name = CharField()  # имя пользователя
    phone = CharField()  # телефон пользователя
    uvedl = CharField()  # вкл/выкл новости, увеломления о новых товарах, скидках и тд, изначально = 1
    orders = CharField()  # совершенные заказы
    sendmes = CharField()  # если отправляет сообщение
    bin = CharField()  # корзина на данный момент
    total = CharField()  # итоговая стоимость корзины
    kolvo = CharField()  # кол-во товаров в корзине
    tov = CharField()  # товаров/товара
    doppredl = CharField()  # доп предложения
    last_total = CharField()  # id последнего сообщения, где был тотал

    class Meta:
        database = db


class Order(Model):
    id = CharField()  # id заказа
    user = CharField()  # заказчик
    phone = CharField()  # телефон заказчика
    bin = CharField()  # корзина товара
    total = CharField()  # итоговая стоимость покупки
    status = CharField()  # статус 0 - оформлен, 1 - подтвержден, 2 - получен
    time = CharField()  # время доставки

    class Meta:
        database = db

db.connect()
#db.create_tables([Product, User, Order])
