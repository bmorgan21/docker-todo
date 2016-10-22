import click

from todo_app import app
from todo_app.models import db


@app.cli.command()
@click.option('--uri', default=None)
def initdb(uri):
    """Initialize the database."""

    if uri is not None:
        app.config['SQLALCHEMY_DATABASE_URI'] = uri

    db.create_all()
