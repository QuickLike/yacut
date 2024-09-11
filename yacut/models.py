import re
from datetime import datetime

from flask import url_for

from settings import Short, Original, CUT_FUNCTION, ViewMessage
from . import db
from .error_handlers import InvalidAPIUsage
from .utils import get_unique_short


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
            short_link=url_for(
                CUT_FUNCTION,
                short=self.short,
                _external=True,
            )
        )

    @classmethod
    def check_short(cls, short: str):
        return re.match(Short.REGEX, short)

    @classmethod
    def get_by_short(cls, short: str, or_404=False):
        if or_404:
            return cls.query.filter_by(short=short).first_or_404()
        return cls.query.filter_by(short=short).first()

    @classmethod
    def create(cls, original: str, short: str = ''):
        if not cls.check_short(short):
            raise InvalidAPIUsage(ViewMessage.SHORT_INVALID)
        url = cls(original=original, short=short or get_unique_short())
        db.session.add(url)
        db.session.commit()
        return url
