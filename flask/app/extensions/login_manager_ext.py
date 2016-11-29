import base64
from flask import current_app, g, request
from flask_login import LoginManager, user_logged_in
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as TimedSerializer,
                          JSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
import random
import string

from app.services.user_service import UserService

login_manager = LoginManager()


def login_user(user):
    if current_app.config['LIMIT_TO_ONE_SESSION']:
        user.tick += 1
    login_manager.reload_user(user=user)
    user_logged_in.send(current_app._get_current_object(), user=user)
    return generate_auth_token(user)


def _dump(secret, d, salt=None, expires_in=None):
    if expires_in:
        s = TimedSerializer(secret, expires_in=expires_in)
    else:
        s = Serializer(secret)
    return s.dumps(d, salt=salt)


def _load(secret, value, salt=None):
    if value is not None:
        s = Serializer(secret)
        try:
            return s.loads(value, salt=salt)
        except SignatureExpired:
            pass  # valid, but expired
        except BadSignature:
            pass  # invalid

    return None


def generate_auth_token(user):
    return _dump(current_app.config['SECRET_KEY'], {'i': user.id, 't': user.tick}, salt=g.secret)


def verify_auth_token(token):
    d = _load(current_app.config['SECRET_KEY'], token, salt=g.secret)
    if d:
        user = UserService.get(d.get('i'), raise_not_found=False)
        if user:
            return user if user.tick == d.get('t') else None
    return None


def _random_secret():
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))


def _init_secret():
    secret = _load(current_app.config['SECRET_KEY'], request.cookies.get(current_app.config['SECRET_COOKIE_NAME']))
    if secret is None:
        secret = _random_secret()

    g.secret = secret


def _set_secret_cookie(response):
    response.set_cookie(current_app.config['SECRET_COOKIE_NAME'],
                        value=_dump(current_app.config['SECRET_KEY'], g.secret, expires_in=current_app.config['SECRET_COOKIE_MAX_AGE']),
                        max_age=current_app.config['SECRET_COOKIE_MAX_AGE'],
                        secure=current_app.config['SECRET_COOKIE_SECURE'], httponly=True)
    return response


@login_manager.request_loader
def load_user_from_request(request):
    user = None
    token = request.args.get('token')

    if not token:
        value = request.headers.get('Authorization')
        if value:
            value = value.replace('Basic ', '', 1)
            try:
                token = base64.b64decode(value).replace(':', '')
            except TypeError:
                pass

    if token:
        user = verify_auth_token(token)

    return user


def init_app(app):
    login_manager.init_app(app)
    app.before_request(_init_secret)
    app.after_request(_set_secret_cookie)
    app.register_extension(login_manager, 'flask-login')
