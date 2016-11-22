from flask import Blueprint, render_template, redirect, request, current_app, session, url_for
from flask_login import login_user, logout_user, current_user
from flask_principal import identity_changed, Identity, AnonymousIdentity

from ct_core_api.core.database import db

from app.services.user_service import UserService

bp = Blueprint('view.auth', __name__)


@bp.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(request.args.get('next', '/'))

    errors = {}
    if request.method == 'POST':
        user = UserService.get(email=request.form['email'], raise_not_found=False)

        if user:
            if UserService.check_password(user.password, request.form['password']):
                login_user(user)
                identity_changed.send(
                    current_app._get_current_object(), identity=Identity(user.id))
                return redirect(request.args.get('next', '/'))
            elif UserService.check_password(user.temp_password, request.form['password']):
                # these are only good once
                UserService.set_password(user, None, attr='temp_password')
                login_user(user)
                identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))

                db.session.commit()
                return redirect(url_for('view.user.change_password', next=request.args.get('next')))
            else:
                errors = {'password': 'Invalid email or password'}
        else:
            errors = {'password': 'Invalid email or password'}

    return render_template('auth/login.html', vars=request.form, errors=errors)


@bp.route("/logout")
def logout():
    logout_user()

    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    # Tell Flask-Principal the user is anonymous
    identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())

    return redirect(request.args.get('next', '/'))


@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(request.args.get('next', '/'))

    errors = {}
    if request.method == 'POST':
        user = UserService.create(
            request.form['email'],
            request.form['password'],
            first_name=request.form['first_name'],
            last_name=request.form['last_name'])

        db.session.add(user)
        db.session.commit()

        login_user(user)
        identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))

        return redirect(request.args.get('next', '/'))

    return render_template('auth/signup.html', vars=request.form, errors=errors)


@bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(request.args.get('next', '/'))

    errors = {}
    if request.method == 'POST':
        user = UserService.send_reset_password(request.form['email'])

        if not user:
            errors['email'] = 'Email not found.'
        else:
            # temp password was generated
            db.session.commit()

            return redirect(url_for('view.auth.login', next=request.args.get('next', '/')))

    return render_template('auth/forgot_password.html', vars=request.form, errors=errors)
