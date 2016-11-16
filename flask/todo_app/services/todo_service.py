from app.lib.model_manager import SqlAlchemyModelManager
from app.models.todo_models import Todo
from app.services import Service

__all__ = ['TodoService']


class TodoManager(SqlAlchemyModelManager):
    __model__ = Todo


class TodoService(Service):
    __manager__ = TodoManager
