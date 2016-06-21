# -*- coding: utf-8 -*-
import datetime

import telebot
import cherrypy

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
           "лета. Осталось проебать {}".format(days_spent, days_left)
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda message: True, commands=['ban'])
def send_statistic(message):
    """BAN person for 5 minutes (or custom period of time)"""
    pass

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
