from .action import Action
from .bot_user import BotUser
from database import db

db.generate_mapping(check_tables=True, create_tables=True)
