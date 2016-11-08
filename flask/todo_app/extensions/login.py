from flask_login import LoginManager

from todo_app.services import UserService

login_manager = LoginManager()
login_manager.login_view = "view.auth.login"


@login_manager.user_loader
def load_user(id):
    return UserService.get(id, raise_not_found=False)
