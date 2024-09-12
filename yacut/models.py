import re
from datetime import datetime
from random import choices

from flask import url_for
from wtforms.validators import ValidationError

from settings import Short, Original, CUT_FUNCTION, ViewMessage
from . import db


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
        for _ in range(Short.MAX_ATTEMPTS):
            short = ''.join(choices(Short.CHARS, k=Short.LENGTH))
            if not URLMap.get(short):
                return short
        raise TimeoutError(Short.GENERATE_ERROR)

    @staticmethod
    def get(short: str, or_404=False):
        url_maps = URLMap.query.filter_by(short=short)
        if or_404:
            return url_maps.first_or_404()
        return url_maps.first()

    @staticmethod
    def create(original: str, short: str):
        if short:
            if len(short) > Short.LENGTH or not re.match(Short.REGEX, short):
                raise ValidationError(ViewMessage.SHORT_INVALID)
            if URLMap.get(short):
                raise ValidationError(ViewMessage.SHORT_EXISTS)
        else:
            short = URLMap.get_unique_short()
        url_map = URLMap(
            original=original,
            short=short
        )
        db.session.add(url_map)
        db.session.commit()
        return url_map
