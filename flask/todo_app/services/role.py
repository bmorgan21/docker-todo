from todo_app.models import Role


def get_all_for_user_id(user_id):
    return Role.get_all_for_user_id(user_id)
