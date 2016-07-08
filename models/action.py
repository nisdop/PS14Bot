from datetime import datetime

from pony.orm import *

from database import db
from .bot_user import BotUser


class Action(db.Entity):
    _table_ = 'actions'
    user = Required(BotUser)
    chat_type = Required(str)
    command_name = Required(str)
    timestamp = Required(datetime, auto=True)
    response = Optional(str)
