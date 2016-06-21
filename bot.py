# -*- coding: utf-8 -*-
import datetime
import random

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

@bot.message_handler(func=lambda message: True, commands=['tits'])
def send_statistic(message):
    """Show me your kitis!"""
    tits = ["https://s-media-cache-ak0.pinimg.com/236x/b5/74/b1/b574b154616e8d0c6d76efaa9de3a0a9.jpg",
        "https://s-media-cache-ak0.pinimg.com/236x/a2/2b/86/a22b863d140d6317e94232f5b9398845.jpg",
        "http://thumbs.bignudeboobs.com/th/2016-01-19/333779_02.jpg",
        "http://girl-tits.com/wp-content/uploads/2015/03/big-tits_-121.jpg",
        "https://s-media-cache-ak0.pinimg.com/236x/7d/45/ca/7d45ca8f28308250170573ca5ff4672c.jpg",
        "https://pp.vk.me/c627530/v627530910/1a8f0/ksAsOAjXys0.jpg",
        "http://amateurinaction.com/wp-content/uploads/2012/04/photo-Babe-Big-Tits-Blonde-409014524.jpg",
        "http://hotfmodels.com/wp-content/uploads/2013/10/tqJBLD0.jpg",
        "http://www.dirtyrottenwhore.com/wp-content/uploads/2015/03/Busty-Gorgeous-Shaved-Teen-Brunette-Babe-Yara-with-Perfect-Breasts-04.png",
        "http://www.18porno.tv/contents/videos_screenshots/0/626/preview.mp4.jpg"]
    rand = random.randint(0, len(tits) - 1)
    bot.send_message(message.chat.id, tits[rand])

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
