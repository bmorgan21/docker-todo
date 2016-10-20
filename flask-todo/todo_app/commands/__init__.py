from todo_app import app
from todo_app.models import db


@app.cli.command()
def initdb():
    """Initialize the database."""
    db.create_all()
