from flask_wtf import FlaskForm
from wtforms import URLField, SubmitField
from wtforms.fields.simple import StringField
from wtforms.validators import DataRequired, Length, Optional, URL


class URLForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(1, 256),
            URL(require_tld=True, message='Некорректный формат ссылки'),
        ]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Optional(),
            Length(1, 16),
        ]
    )
    submit = SubmitField('Создать')
