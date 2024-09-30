import re
from datetime import datetime
from random import choices

from flask import url_for

from settings import Short, Original, CUT_FUNCTION, ViewMessage
from . import db


class URLMap(db.Model):
    class LimitReached(Exception):
        pass

    class InvalidShort(Exception):
        pass

    class InvalidURL(Exception):
        pass

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(
        db.String(Original.LENGTH),
        unique=True,
        nullable=False
    )
    short = db.Column(db.String(Short.LENGTH), unique=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=URLMap.short_link(self.short)
        )

    @staticmethod
    def short_link(short):
        return url_for(
            CUT_FUNCTION,
            short=short,
            _external=True,
        )

    @staticmethod
    def get_unique_short() -> str:
        for _ in range(Short.MAX_ATTEMPTS):
            short = ''.join(choices(Short.CHARS, k=Short.LENGTH))
            if not URLMap.get(short):
                return short
        raise URLMap.LimitReached(Short.GENERATE_ERROR)

    @staticmethod
    def get(short: str, or_404=False):
        url_maps = URLMap.query.filter_by(short=short)
        if or_404:
            return url_maps.first_or_404()
        return url_maps.first()

    @staticmethod
    def create(original: str, short: str, validate=False):
        if validate and len(original) > Original.LENGTH:
            raise URLMap.InvalidURL(ViewMessage.URL_INVALID)
        if not short:
            short = URLMap.get_unique_short()
        else:
            if (
                len(short) > Short.LENGTH or
                not re.match(Short.REGEX, short)
            ):
                raise URLMap.InvalidShort(ViewMessage.SHORT_INVALID)
            if URLMap.get(short):
                raise URLMap.InvalidShort(ViewMessage.SHORT_EXISTS)
        url_map = URLMap(
            original=original,
            short=short
        )
        db.session.add(url_map)
        db.session.commit()
        return url_map
