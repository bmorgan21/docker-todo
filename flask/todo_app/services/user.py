from todo_app.models import db, User

import bcrypt


def set_password(user, plain_text_password):
    user.password = bcrypt.hashpw(plain_text_password, bcrypt.gensalt())


def check_password(user, plain_text_password):
    return bcrypt.checkpw(plain_text_password, user.password)


def get(id):
    return User.get(id)


def get_by_email(email):
    return User.get_by_email(email)


def create(email, password, first_name=None, last_name=None):
    user = User(first_name=first_name, last_name=last_name, email=email)
    set_password(user, password)

    db.session.add(user)

    return user
