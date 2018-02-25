# -*- coding: utf-8 -*-

import config
import bottoken
import telebot

bot = telebot.TeleBot(bottoken.mytoken)


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, message.text)


if __name__ == '__main__':
    bot.polling(none_stop=True)
