import re
from datetime import datetime
from random import shuffle

from flask import url_for

from settings import Short, Original, CUT_FUNCTION, ViewMessage
from . import db
from .error_handlers import InvalidUsage


class URLMap(db.Model):
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
        chars = list(Short.CHARS)
        shuffle(chars)
        short = ''.join(chars)[:Short.LENGTH]
        if URLMap.get(short):
            short = URLMap.get_unique_short()
        return str(short)

    @staticmethod
    def get(short: str, or_404=False):
        if or_404:
            return URLMap.query.filter_by(short=short).first_or_404()
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def create(original: str, short: str = '', form=None):
        error = False
        url_map = None
        if form is not None:
            if not re.match(Short.REGEX, short):
                form.custom_id.errors = [
                    ViewMessage.SHORT_INVALID
                ]
                error = True
            if URLMap.get(short):
                form.custom_id.errors = [
                    ViewMessage.SHORT_EXISTS
                ]
                error = True
        else:
            if not re.match(Short.REGEX, short):
                raise InvalidUsage(ViewMessage.SHORT_INVALID)
            if URLMap.get(short):
                raise InvalidUsage(ViewMessage.SHORT_EXISTS)
        if not error:
            url_map = URLMap(
                original=original,
                short=short or URLMap.get_unique_short()
            )
            db.session.add(url_map)
            db.session.commit()
        return url_map, form
