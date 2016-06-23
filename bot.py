# -*- coding: utf-8 -*-
import datetime
import random
from urllib import request
from threading import Timer

import telebot
import cherrypy
from bs4 import BeautifulSoup

import config
from server import WebhookServer

WEBHOOK_HOST = config.SERVER_IP
WEBHOOK_PORT = config.WEBHOOK_PORT
WEBHOOK_LISTEN = config.WEBHOOK_LISTEN

WEBHOOK_SSL_CERT = config.WEBHOOK_SSL_CERT
WEBHOOK_SSL_PRIV = config.WEBHOOK_SSL_PRIV

WEBHOOK_URL_BASE = "https://{}:{}".format(WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(config.TOKEN)

bot = telebot.TeleBot(config.TOKEN)

banned_users =[]


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
    soup = BeautifulSoup(html)
    img = soup.findAll('img', {'alt': 'boobs-selfshots.tumblr.com'})
    link = img[0]['src']
    bot.send_message(message.chat.id, link)


@bot.message_handler(func=lambda message: True, commands=['/ban'])
def ban_user(message):
    user_id = message.user.id
    chat_id = message.chat.id
    bot.kick_chat_member(chat_id, user_id)
    banned_users.append([chat_id, user_id])
    t = Timer(300.0, unban_user)
    t.start()


@bot.message_handler(func=lambda message: True, commands=['/unban'])
def manual_unban_user(message):
    bot.unban_chat_member(message.chat.id, message.user.id)


def unban_user():
    if len(banned_users) > 0:
        ban = banned_users[0]
        bot.unban_chat_member(ban[0], ban[1])
        banned_users.pop(ban)


bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))

cherrypy.config.update({
    'server.socket_host': WEBHOOK_LISTEN,
    'server.socket_port': WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': WEBHOOK_SSL_CERT,
    'server.ssl_private_key': WEBHOOK_SSL_PRIV
})

cherrypy.quickstart(WebhookServer(bot), WEBHOOK_URL_PATH, {'/': {}})
