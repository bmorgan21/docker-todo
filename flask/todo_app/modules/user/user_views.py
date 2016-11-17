from flask import Blueprint, render_template, redirect, request
from flask_login import login_required, current_user

from ct_core_api.core.database import db

from todo_app.services.user_service import UserService

bp = Blueprint('view.user', __name__)


@bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    user = UserService.get(current_user.id)

    errors = {}
    if request.method == 'POST':
        if not request.form['password'] or len(request.form['password']) < 5:
            errors['password'] = 'Invalid, password must be at least 5 characters'
        elif request.form['password'] != request.form['confirm_password']:
            errors['confirm_password'] = 'Passwords do not match'

        if len(errors) == 0:
            UserService.set_password(user, request.form['password'])

            db.session.commit()

            return redirect(request.args.get('next', '/'))

    return render_template('user/change_password.html', vars=request.form, errors=errors)


@bp.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    errors = {}
    if request.method == 'POST':
        form_vars = request.form

        UserService.update(current_user.id, {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email']})

        db.session.commit()

        return redirect(request.args.get('next', '/'))
    else:
        user = UserService.get(current_user.id)

        form_vars = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }

    return render_template('user/account.html', vars=form_vars, errors=errors)
