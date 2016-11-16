from flask_login import current_user
from flask_principal import Permission, RoleNeed, UserNeed, identity_loaded

from ct_core_api.api.app.extensions.login_manager_ext import login_manager

from app import enums
from app.services.user_service import UserService

admin_permission = Permission(RoleNeed(enums.Role.ADMIN))


@identity_loaded.connect
def on_identity_loaded(sender, identity):
    # Set the identity user object
    identity.user = current_user

    # Add the UserNeed to the identity
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))

        roles = UserService.get_roles(current_user.id)
        for role in roles:
            identity.provides.add(RoleNeed(role.name))


@login_manager.user_loader
def load_user(id):
    return UserService.get(id, raise_not_found=False)


def init_app(app):
    from app.modules.auth import auth_views
    app.register_blueprint(auth_views.bp, url_prefix='/auth')
    login_manager.login_view = 'view.auth.login'
