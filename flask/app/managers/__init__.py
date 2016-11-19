from model_manager import SqlAlchemyModelManager
from app.models.todo_models import (
    Role,
    Todo,
    User
)


class RoleManager(SqlAlchemyModelManager):
    __model__ = Role


class TodoManager(SqlAlchemyModelManager):
    __model__ = Todo


class UserManager(SqlAlchemyModelManager):
    __model__ = User

    @staticmethod
    def add_role(user_id, name):
        return RoleManager.create(user_id=user_id, name=name)

    @staticmethod
    def get_roles(user_id):
        return RoleManager.get_many(user_id=user_id)
