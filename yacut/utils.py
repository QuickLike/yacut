from random import choice

from settings import Short


def get_unique_short():
    short = ''
    for _ in range(Short.LENGTH):
        short += choice(Short.CHARS)
    return short
