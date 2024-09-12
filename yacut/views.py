from flask import render_template, redirect

from . import app
from .forms import URLForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    url_map, form.custom_id.errors = URLMap.create(
        form.original_link.data,
        form.custom_id.data
    )
    return render_template(
        'index.html',
        form=form,
        short_url=URLMap.short_link(url_map.short if url_map else None),
    )


@app.route('/<short>', methods=['GET'])
def cut_url_view(short):
    return redirect(
        URLMap.get(short, True).original
    )
