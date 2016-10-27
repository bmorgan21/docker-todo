from datetime import datetime, timedelta
from random import choice

from todo_app.models import db, User
from todo_app.services import email as email_svc

import bcrypt


charsets = [
    'abcdefghijklmnopqrstuvwxyz',
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
    '0123456789',
    '^!\$%&/()=?{[]}+~#-_.:,;<>|\\',
]


def mkpassword(length=16):
    pwd = []
    charset = choice(charsets)
    while len(pwd) < length:
        pwd.append(choice(charset))
        charset = choice(list(set(charsets) - set([charset])))
    return "".join(pwd)


def set_password(user, plain_text_password, attr='password'):
    if plain_text_password:
        value = bcrypt.hashpw(plain_text_password, bcrypt.gensalt())
    else:
        value = None

    setattr(user, attr, value)

    if value and attr == 'password':
        user.password_expires = datetime.utcnow() + timedelta(days=365)


def check_password(password, plain_text_password):
    return password and plain_text_password and bcrypt.checkpw(plain_text_password, password)


def get(id):
    return User.get(id)


def get_by_email(email):
    return User.get_by_email(email)


def create(email, password, first_name=None, last_name=None):
    user = User(first_name=first_name, last_name=last_name, email=email)
    set_password(user, password)

    db.session.add(user)

    return user


def send_reset_password(email):
    user = get_by_email(email)
    if user:
        # give them a new password they can use to login with
        password = mkpassword()
        set_password(user, password, attr='temp_password')
        email_svc.send_reset_password(user, password)

    return user
