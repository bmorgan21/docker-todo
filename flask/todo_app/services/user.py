from datetime import datetime, timedelta
from random import choice

from todo_app.services import Service, email as email_svc
from todo_app.managers import UserManager

import bcrypt

__all__ = ['UserService']


charsets = [
    'abcdefghijklmnopqrstuvwxyz',
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
    '0123456789',
    '^!\$%&/()=?{[]}+~#-_.:,;<>|\\',
]


class UserService(Service):
    __manager__ = UserManager

    @staticmethod
    def _mkpassword(length=16):
        pwd = []
        charset = choice(charsets)
        while len(pwd) < length:
            pwd.append(choice(charset))
            charset = choice(list(set(charsets) - set([charset])))
        return "".join(pwd)

    @staticmethod
    def set_password(user, plain_text_password, attr='password'):
        if plain_text_password:
            value = bcrypt.hashpw(plain_text_password, bcrypt.gensalt())
        else:
            value = None

        setattr(user, attr, value)

        if value and attr == 'password':
            user.password_expires = datetime.utcnow() + timedelta(days=365)

    @staticmethod
    def check_password(password, plain_text_password):
        return password and plain_text_password and bcrypt.checkpw(plain_text_password, password)

    @classmethod
    def create(cls, email, password, first_name=None, last_name=None):
        user = cls.__manager__.create(first_name=first_name, last_name=last_name, email=email)
        cls.set_password(user, password)
        return user

    @classmethod
    def send_reset_password(cls, email):
        user = cls.get(email=email, raise_not_found=False)
        if user:
            # give them a new password they can use to login with
            password = cls._mkpassword()
            cls.set_password(user, password, attr='temp_password')
            email_svc.send_reset_password(user, password)

        return user
