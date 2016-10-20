from todo_app.models import db


class User(db.Model):
    first_name = db.Column(db.Unicode(16))
    last_name = db.Column(db.Unicode(16))
    email = db.Column(db.Email, nullable=False, unique=True)
