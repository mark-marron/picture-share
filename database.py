from sqlite3 import *
from flask import g
import os

DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), "database.db")

def get_db():
    if "db" not in g:
        g.db = connect(DATABASE, detect_types=PARSE_DECLTYPES)
        g.db.row_factory = Row
    return g.db

def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()