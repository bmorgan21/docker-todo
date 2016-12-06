from datetime import datetime, timedelta
from random import choice

import bcrypt

from app.managers import UserManager
from app.services import Service

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
            charset = choice(list(set(charsets) - {charset}))
        return "".join(pwd)

    @staticmethod
    def _set_password(user, plain_text_password, attr='password'):
        if plain_text_password:
            value = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
        else:
            value = None

        setattr(user, attr, value)

        if value and attr == 'password':
            user.password_expires = datetime.utcnow() + timedelta(days=365)

    @staticmethod
    def check_password(password, plain_text_password):
        return password and plain_text_password and bcrypt.checkpw(plain_text_password.encode('utf-8'), password.encode('utf-8'))

    @classmethod
    def create(cls, **kwargs):
        password = kwargs.pop('password', None)
        user = cls.__manager__.create(**kwargs)
        if password:
            cls._set_password(user, password)
        return user

    @classmethod
    def update(cls, id, d):
        password = d.pop('password', None)
        user = cls.__manager__.update(id, d)
        if password:
            cls._set_password(user, password)
        return user

    @classmethod
    def send_reset_password(cls, email):
        from app.services import email_service
        user = cls.get(email=email, raise_not_found=False)
        if user:
            # give them a new password they can use to login with
            password = cls._mkpassword()
            cls._set_password(user, password, attr='temp_password')
            email_service.send_reset_password(user, password)

        return user
