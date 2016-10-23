from flask import Blueprint, render_template, redirect, request
from flask_login import login_user, logout_user, login_required, current_user

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
            return redirect(request.args.get('next', '/'))
        else:
            errors = {'password': 'Invalid email or password'}

    return render_template('login.html', vars=request.form, errors=errors)


@bp.route("/logout")
def logout():
    logout_user()
    return redirect('/')


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
        return redirect(request.args.get('next', '/'))

    return render_template('signup.html', vars=request.form, errors=errors)
