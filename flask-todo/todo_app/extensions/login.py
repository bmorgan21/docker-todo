from flask_login import LoginManager

from todo_app.services import user as user_svc

login_manager = LoginManager()
login_manager.login_view = "view.auth.login"


@login_manager.user_loader
def load_user(id):
    return user_svc.get(id)
