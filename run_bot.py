import cherrypy

import config
from bot import bot
from server import WebhookServer

bot.remove_webhook()
bot.set_webhook(url="https://{}:{}/{}/".format(config.SERVER_IP,
                                               config.WEBHOOK_PORT,
                                               config.TOKEN,
                                               ),
                certificate=open(config.WEBHOOK_SSL_CERT, 'r'))

cherrypy.config.update({
    'server.socket_host': config.WEBHOOK_LISTEN,
    'server.socket_port': config.WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': config.WEBHOOK_SSL_CERT,
    'server.ssl_private_key': config.WEBHOOK_SSL_PRIV
})

cherrypy.quickstart(WebhookServer(bot), "/{}/".format(config.TOKEN), {'/': {}})
