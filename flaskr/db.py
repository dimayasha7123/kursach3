import psycopg2
import click
from flask import current_app, g
from flask.cli import with_appcontext
from scripts.load_cats_and_themes import load_initial_data_from_csv


def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(current_app.config['DSN'])
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def init_db():
    db = get_db()
    load_initial_data_from_csv(db, '.\scripts\dataset1.csv')


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')
