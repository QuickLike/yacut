import os
from string import ascii_letters, digits


SHORT_ID_LENGTH = 6
SHORT_ID_CHARS = ascii_letters + digits


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')
