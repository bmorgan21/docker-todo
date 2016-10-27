from todo_app import enums
from todo_app.models import db

__all__ = ['User', 'Role']


class User(db.Model):
    first_name = db.Column(db.Unicode(16))
    last_name = db.Column(db.Unicode(16))
    email = db.Column(db.Email, nullable=False, unique=True)
    password = db.Column(db.UnicodeText)
    temp_password = db.Column(db.UnicodeText)
    password_expires = db.Column(db.DateTime)

    def __str__(self):
        return '{} {} ({})'.format(self.first_name, self.last_name, self.email)

    ###
    # Properties required by Flask-Login
    ##

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    ###

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter(cls.email == email).first()


class Role(db.Model):
    user_id = db.Column(db.ObjectID, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.Enum(enums.Role, 16))

    @classmethod
    def get_all_for_user_id(cls, user_id):
        q = cls.query \
               .filter(cls.user_id == user_id)

        return q.all()
