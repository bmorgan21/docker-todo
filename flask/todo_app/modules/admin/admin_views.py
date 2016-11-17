from flask import redirect, url_for, request
from flask_admin import Admin, AdminIndexView as BaseAdminIndexView
from flask_admin.contrib.sqla import ModelView as BaseModelView
from flask_login import current_user

from ct_core_api.core.database import db

from todo_app.models import todo_models, user_models


class AuthView(object):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('view.auth.login', next=request.url))


class ModelView(AuthView, BaseModelView):
    pass


class AdminIndexView(AuthView, BaseAdminIndexView):
    pass


admin = Admin(index_view=AdminIndexView(), template_mode='bootstrap3')
admin.add_view(ModelView(todo_models.Todo, db.session))
admin.add_view(ModelView(user_models.User, db.session))
admin.add_view(ModelView(user_models.Role, db.session))
