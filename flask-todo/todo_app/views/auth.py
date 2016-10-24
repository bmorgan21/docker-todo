from flask import Blueprint, render_template, redirect, request, current_app, session
from flask_login import login_user, logout_user, current_user
from flask_principal import identity_changed, Identity, AnonymousIdentity

from todo_app.models import db
from todo_app.services import user as user_svc

bp = Blueprint('view.auth', __name__)


@bp.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(request.args.get('next', '/'))

    errors = {}
    if request.method == 'POST':
        user = user_svc.get_by_email(request.form['email'])

        if user and user_svc.check_password(user, request.form['password']):
            login_user(user)
            identity_changed.send(current_app._get_current_object(),
                                  identity=Identity(user.id))
            return redirect(request.args.get('next', '/'))
        else:
            errors = {'password': 'Invalid email or password'}

    return render_template('login.html', vars=request.form, errors=errors)


@bp.route("/logout")
def logout():
    logout_user()

    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    # Tell Flask-Principal the user is anonymous
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())

    return redirect(request.args.get('next', '/'))


@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(request.args.get('next', '/'))

    errors = {}
    if request.method == 'POST':
        user = user_svc.create(request.form['email'], request.form['password'],
                               first_name=request.form['first_name'], last_name=request.form['last_name'])

        db.session.commit()

        login_user(user)
        identity_changed.send(current_app._get_current_object(),
                              identity=Identity(user.id))

        return redirect(request.args.get('next', '/'))

    return render_template('signup.html', vars=request.form, errors=errors)
