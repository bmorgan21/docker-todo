from todo_app.models import db

__all__ = ['Todo']


class Todo(db.Model):
    name = db.Column(db.UnicodeText)
    is_complete = db.Column(db.Boolean, nullable=False, default=True)

    @classmethod
    def get(cls, id):
        return cls.query.get(id)

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def delete(cls, id):
        cls.query.filter(cls.id == id).delete()
