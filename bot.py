# -*- coding: utf-8 -*-
import datetime
from urllib import request

import telebot
from bs4 import BeautifulSoup
from pony.orm import *

from config import TOKEN
from models import Action, BotUser

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(func=lambda message: True, commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, 'You shall not pass!')
    log_action(message)


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
    log_action(message)


@bot.message_handler(func=lambda message: True, commands=['tits'])
def send_tits(message):
    random_tits_url = 'http://boobs-selfshots.tumblr.com/random'
    response = request.urlopen(random_tits_url)
    html = response.read()
    soup = BeautifulSoup(html, "html.parser")
    img = soup.findAll('div', {'class': 'photo_post'})[0].a.img
    link = img['src']
    bot.send_message(message.chat.id, link)
    log_action(message, link)


@db_session
def log_action(message, response=None):
    try:
        user = BotUser[message.from_user.id]
    except ObjectNotFound:
        user = BotUser(first_name=message.from_user.first_name,
                       last_name=message.from_user.last_name,
                       id=message.from_user.id,
                       username=message.from_user.username
                       )
    action = Action(user=user, chat_type=message.chat.type,
                    command_name=message.text[1:], response=response
                    )
