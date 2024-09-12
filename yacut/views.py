from flask import render_template, redirect, flash

from . import app
from .forms import URLForm
from .models import URLMap, InvalidShort, InvalidURL, LimitReached


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        return render_template(
            'index.html',
            form=form,
            short_url=URLMap.short_link(
                URLMap.create(
                    form.original_link.data,
                    form.custom_id.data
                ).short
            ),
        )
    except (InvalidShort, InvalidURL, LimitReached) as e:
        flash(str(e))
        return render_template('index.html', form=form)


@app.route('/<short>', methods=['GET'])
def cut_url_view(short):
    return redirect(
        URLMap.get(short, True).original
    )
