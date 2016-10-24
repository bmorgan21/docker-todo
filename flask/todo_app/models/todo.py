from todo_app.models import db

__all__ = ['Todo']


class Todo(db.Model):
    name = db.Column(db.UnicodeText)
    is_complete = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.ObjectID, db.ForeignKey('user.id'), nullable=False)
