from ct_core_api.core.database import db
from flask.ext.login import UserMixin

from app import enums

__all__ = ['User', 'Role']


class User(db.Model, UserMixin):
    first_name = db.Column(db.Unicode(16))
    last_name = db.Column(db.Unicode(16))
    email = db.Column(db.Email, nullable=False, unique=True)
    password = db.Column(db.UnicodeText)
    temp_password = db.Column(db.UnicodeText)
    password_expires = db.Column(db.DateTime)

    def __str__(self):
        return '{} {} ({})'.format(self.first_name, self.last_name, self.email)

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter(cls.email == email).first()


class Role(db.Model):
    user_id = db.Column(db.ObjectID, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.Enum(enums.Role, 16))

    @classmethod
    def get_all_for_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()
