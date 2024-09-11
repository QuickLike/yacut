from flask import render_template, redirect, url_for

from settings import ViewMessage, Short, CUT_FUNCTION
from . import app
from .forms import URLForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)

    short = form.custom_id.data or ''

    if URLMap.get_by_short(short):
        form.custom_id.errors = [
            ViewMessage.SHORT_EXISTS
        ]
        return render_template('index.html', form=form)
    if not URLMap.check_short(short):
        form.custom_id.errors = [
            ViewMessage.SHORT_INVALID
        ]
        return render_template('index.html', form=form)

    url = URLMap.create(form.original_link.data, short)
    return render_template(
        'index.html',
        form=form,
        message=Short.URL_READY.format(
            short_url=url_for(
                CUT_FUNCTION,
                short=url.short,
                _external=True,
            )
        )
    )


@app.route('/<short>', methods=['GET'])
def cut_url_view(short):
    return redirect(
        URLMap.get_by_short(short, True).original
    )
