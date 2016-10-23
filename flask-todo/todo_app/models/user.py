from todo_app.models import db

__all__ = ['User', 'Role', 'UserRole']


class User(db.Model):
    first_name = db.Column(db.Unicode(16))
    last_name = db.Column(db.Unicode(16))
    email = db.Column(db.Email, nullable=False, unique=True)
    password = db.Column(db.UnicodeText)

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
    name = db.Column(db.Unicode(16))


class UserRole(db.Model):
    __table_args__ = (
        db.PrimaryKeyConstraint('user_id', 'role_id'),
    )

    id = None

    user_id = db.Column(db.ObjectID, db.ForeignKey('user.id'), nullable=False)
    role_id = db.Column(db.ObjectID, db.ForeignKey('role.id'), nullable=False)
