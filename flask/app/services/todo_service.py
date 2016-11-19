from app.managers import TodoManager
from app.services import Service

__all__ = ['TodoService']


class TodoService(Service):
    __manager__ = TodoManager
