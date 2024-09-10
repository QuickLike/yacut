import shutil

import click

from . import app


@app.cli.command('clear_db')
def clear_db_command():
    """Функция удаления базы данных и всех миграций."""
    try:
        shutil.rmtree('instance')
        shutil.rmtree('migrations')
        click.echo('База данных удалена')
    except Exception as e:
        click.echo(f'Ошибка: {e}')
