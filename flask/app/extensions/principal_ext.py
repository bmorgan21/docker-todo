from flask_principal import Principal

from flask_login import current_user, user_loaded_from_request, user_logged_in
from flask_principal import Permission, RoleNeed, UserNeed, identity_loaded, identity_changed, Identity

from app import enums
from app.services.user_service import UserService

principal = Principal(use_sessions=False, skip_static=True)

admin_permission = Permission(RoleNeed(enums.Role.ADMIN))


@user_loaded_from_request.connect
def on_user_loaded(sender, user):
    identity_changed.send(sender, identity=Identity(user.id))


@user_logged_in.connect
def on_user_logged_in(sender, user):
    identity_changed.send(sender, identity=Identity(user.id))


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


def init_app(app):
    principal.init_app(app)
    app.register_extension(principal, 'flask-principal')
