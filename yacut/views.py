from flask import render_template, redirect

from . import app
from .forms import URLForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)

    short = form.custom_id.data

    url_map, form = URLMap.create(form.original_link.data, short, form)

    if form.errors:
        short_url = None
    else:
        short_url = URLMap.short_link(url_map.short)

    return render_template(
        'index.html',
        form=form,
        short_url=short_url,
    )


@app.route('/<short>', methods=['GET'])
def cut_url_view(short):
    return redirect(
        URLMap.get(short, True).original
    )
