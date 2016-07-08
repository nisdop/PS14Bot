from pony.orm import *

from database import db


class BotUser(db.Entity):
    _table_ = 'bot_users'
    id = PrimaryKey(int)
    first_name = Optional(str)
    last_name = Optional(str)
    username = Optional(str)
    actions = Set('Action')
