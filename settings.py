import os
from string import ascii_letters, digits


CUT_FUNCTION = 'cut_url_view'

SUBMIT_LABEL = 'Создать'


class Short(object):
    LENGTH = 6
    CHARS = ascii_letters + digits
    REGEX = f'^[{CHARS}]+$'
    LABEL = 'Ваш вариант короткой ссылки'
    MAX_ATTEMPTS = 5


class Original(object):
    LENGTH = 2048
    LABEL = 'Длинная ссылка'
    REQUIRED_MESSAGE = 'Обязательное поле'
    INVALID_FORMAT = 'Некорректный формат ссылки'


class ViewMessage(object):
    ID_NOT_FOUND = 'Указанный id не найден'
    EMPTY_BODY = 'Отсутствует тело запроса'
    URL_REQUIRED = '"url" является обязательным полем!'
    SHORT_EXISTS = 'Предложенный вариант короткой ссылки уже существует.'
    SHORT_INVALID = 'Указано недопустимое имя для короткой ссылки'


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')
