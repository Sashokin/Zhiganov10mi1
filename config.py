# -*- coding: utf-8 -*-
import telebot
from telebot import types
import my_markups
import config_for_token
import sqlite3


conn = sqlite3.connect("database.db")
cursor = conn.cursor()
#cursor.execute("""CREATE TABLE Users (id text, name text, phone text, address text, orders text, rights text)""")

