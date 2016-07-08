from pony.orm import Database

from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER

db = Database('postgres',
              user=DB_USER, password=DB_PASSWORD,
              host='{}'.format(DB_HOST),
              database=DB_NAME
              )
