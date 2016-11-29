from flask_login import UserMixin

from ct_core_api.core.database import db

from app import enums

__all__ = ['User', 'Role']


class User(db.Model, UserMixin):
    first_name = db.Column(db.Unicode(16))
    last_name = db.Column(db.Unicode(16))
    email = db.Column(db.Email, nullable=False, unique=True)
    password = db.Column(db.UnicodeText)
    temp_password = db.Column(db.UnicodeText)
    password_expires = db.Column(db.DateTime)

    tick = db.Column(db.Integer, nullable=False, default=1)


class Role(db.Model):
    user_id = db.Column(db.ObjectID, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.Enum(enums.Role, 16))
