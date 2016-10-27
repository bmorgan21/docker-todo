from flask import redirect, url_for, request
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from todo_app.models import db, Role, Todo, User


class AuthView:
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('view.auth.login', next=request.url))


class MyModelView(AuthView, ModelView):
    pass


class MyAdminIndexView(AuthView, AdminIndexView):
    pass


admin = Admin(index_view=MyAdminIndexView(), template_mode='bootstrap3')
admin.add_view(MyModelView(Role, db.session))
admin.add_view(MyModelView(Todo, db.session))
admin.add_view(MyModelView(User, db.session))
