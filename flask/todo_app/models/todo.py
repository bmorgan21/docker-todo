from todo_app.models import db

__all__ = ['Todo']


class Todo(db.Model):
    name = db.Column(db.UnicodeText)
    is_complete = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.ObjectID, db.ForeignKey('user.id'), nullable=False)

    @classmethod
    def get_all_for_user_id(cls, user_id):
        return cls.query.filter(cls.user_id == user_id).all()
