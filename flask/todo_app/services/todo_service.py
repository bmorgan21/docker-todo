from todo_app.lib.model_manager import SqlAlchemyModelManager
from todo_app.models.todo_models import Todo
from todo_app.services import Service

__all__ = ['TodoService']


class TodoManager(SqlAlchemyModelManager):
    __model__ = Todo


class TodoService(Service):
    __manager__ = TodoManager
