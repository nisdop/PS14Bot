import cherrypy
import telebot


class WebhookServer(object):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    def check_headers(self, headers):
        if 'content-length' not in headers:
            return False

        if 'content-type' not in headers:
            return False

        if headers['content-type'] != 'application/json':
            return False

        return True

    @cherrypy.expose
    def index(self):
        if self.check_headers(cherrypy.request.headers):
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            self.bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)
