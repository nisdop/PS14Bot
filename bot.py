# -*- coding: utf-8 -*-
import datetime
from urllib import request

import telebot
from bs4 import BeautifulSoup

from config import TOKEN


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(func=lambda message: True, commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, 'You shall not pass!')


@bot.message_handler(func=lambda message: True, commands=['stat'])
def send_statistic(message):
    summer_days_count = 92
    today = datetime.datetime.now()
    deadline = today.replace(month=9, day=1, hour=0, minute=0)
    delta_time = deadline - today
    days_left = delta_time.days
    days_spent = summer_days_count - days_left
    text = "На данный момент уже благополучно проёбано {} дней " \
           "лета. Осталось проебать {}.".format(days_spent, days_left)
    bot.send_message(message.chat.id, text)


@bot.message_handler(func=lambda message: True, commands=['tits'])
def send_tits(message):
    random_tits_url = 'http://boobs-selfshots.tumblr.com/random'
    response = request.urlopen(random_tits_url)
    html = response.read()
    soup = BeautifulSoup(html, "html.parser")
    a_tag = soup.findAll('div', {'class': 'photo_post'})[0].a
    if a_tag is not None:
        img = a_tag.img
    else:
        img = soup.findAll('div', {'class': 'photo_post'})[0].img
    link = img['src']
    bot.send_message(message.chat.id, link)



