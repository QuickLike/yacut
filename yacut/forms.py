from flask_wtf import FlaskForm
from wtforms import URLField, SubmitField
from wtforms.fields.simple import StringField
from wtforms.validators import DataRequired, Length, Optional, URL, Regexp

from settings import Original, Short


SUBMIT_LABEL = 'Создать'


class URLForm(FlaskForm):
    original_link = URLField(
        Original.LABEL,
        validators=[
            DataRequired(message=Original.REQUIRED_MESSAGE),
            Length(max=Original.LENGTH),
            URL(require_tld=True, message=Original.INVALID_FORMAT),
        ]
    )
    custom_id = StringField(
        Short.LABEL,
        validators=[
            Optional(),
            Length(max=Short.LENGTH),
            Regexp(Short.REGEX)
        ]
    )
    submit = SubmitField(SUBMIT_LABEL)
