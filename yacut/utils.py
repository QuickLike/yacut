from random import choice

from .models import URLMap
from settings import SHORT_ID_LENGTH, SHORT_ID_CHARS


def get_unique_short_id():
    while True:
        short_id = ''.join(
            [choice(SHORT_ID_CHARS) for _ in range(SHORT_ID_LENGTH)]
        )
        if URLMap.query.filter_by(short=short_id).first():
            continue
        return short_id


def check_custom_id(short_id):
    if len(short_id) > SHORT_ID_LENGTH:
        return False
    for char in short_id:
        if char not in SHORT_ID_CHARS:
            return False
    return True
