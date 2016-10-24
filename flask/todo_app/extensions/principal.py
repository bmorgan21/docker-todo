from flask_login import current_user
from flask_principal import Principal, Permission, RoleNeed, UserNeed, identity_loaded

from todo_app import enums
from todo_app.services import role as role_svc

principals = Principal()

admin_permission = Permission(RoleNeed(enums.Role.ADMIN))


@identity_loaded.connect
def on_identity_loaded(sender, identity):
    # Set the identity user object
    identity.user = current_user

    # Add the UserNeed to the identity
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))

        roles = role_svc.get_all_for_user_id(current_user.id)
        for role in roles:
            identity.provides.add(RoleNeed(role.name))
