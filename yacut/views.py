import re

from flask import flash, render_template, redirect, request

from . import app, db
from .forms import URLForm
from .models import URLMap
from .utils import get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    custom_id = form.custom_id.data
    if not custom_id:
        custom_id = get_unique_short_id()
    if URLMap.query.filter_by(short=custom_id).first():
        form.custom_id.errors = [
            'Предложенный вариант короткой ссылки уже существует.'
        ]
        return render_template('yacut.html', form=form)
    if not re.match(r'^[A-Za-z0-9]{1,16}$', custom_id):
        form.custom_id.errors = [
            'Указано недопустимое имя для короткой ссылки'
        ]
        return render_template('yacut.html', form=form)

    url = form.original_link.data
    if form.validate_on_submit():
        url_map = URLMap.query.filter_by(original=url).first()
        if url_map is not None:
            db.session.delete(url_map)
            db.session.commit()
        url_map = URLMap(
            original=form.original_link.data,
            short=custom_id
        )
        db.session.add(url_map)
        db.session.commit()
        flash(f'Ваша новая ссылка готова:\n'
              f'<a href="{request.base_url}{custom_id}">'
              f'{request.base_url}{custom_id}</a>')
    return render_template('yacut.html', form=form)


@app.route('/<short_id>', methods=['GET'])
def cut_url_view(short_id):
    return redirect(
        URLMap.query.filter_by(short=short_id).first_or_404().original
    )
