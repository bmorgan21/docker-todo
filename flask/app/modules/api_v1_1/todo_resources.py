import logging

from flask_login import current_user, login_required

from ct_core_api.api.core import response
from ct_core_api.api.core.namespace import APINamespace
from ct_core_api.api.core.resource import APIResource
from ct_core_api.api.core.parameters import Parameters
from ct_core_api.core.database import db

from app.schemas import todo_schemas
from app.services.todo_service import TodoService

_logger = logging.getLogger(__name__)

api = APINamespace('todos', description="Todos")


@api.route('/')
class TodoCollectionResource(APIResource):
    @login_required
    @api.response(todo_schemas.TodoSchema(many=True))
    def get(self):
        """Get all Todos."""
        return TodoService.get_many(user_id=current_user.id)

    class PostTodoParameters(Parameters, todo_schemas.TodoSchema):
        pass

    @api.parameters(PostTodoParameters(), locations=['json'])
    @api.response(todo_schemas.TodoSchema())
    @api.response(code=response.Forbidden.code)
    @api.response(code=response.Conflict.code)
    def post(self, args):
        """Create a new Todo."""
        with api.commit_or_abort(db.session, default_error_message=u"Failed to create a new Todo."):
            new_todo = TodoService.create(user_id=current_user.id, **args)
            db.session.add(new_todo)
        return new_todo


@api.route('/<int:id>')
@api.resolve_object_by_find('todo', TodoService.get)
@api.response(code=response.NotFound.code, description=u"Todo not found.")
class TodoResource(APIResource):
    class PatchTodoParameters(Parameters, todo_schemas.TodoSchema):
        pass

    @login_required
    @api.response(todo_schemas.TodoSchema())
    def get(self, todo):
        """Get todo details by id."""
        return todo

    @login_required
    @api.parameters(PatchTodoParameters(), locations=['json'])
    @api.response(todo_schemas.TodoSchema())
    @api.response(code=response.Conflict.code)
    def patch(self, args, todo):
        """Patch todo details by id."""
        with api.commit_or_abort(db.session, default_error_message=u'Failed to update todo details.'):
            TodoService.update(todo, args)
        return todo

    @login_required
    @api.response(code=response.HTTPStatus.NO_CONTENT)
    def delete(self, todo):
        """Delete todo by id."""
        with api.commit_or_abort(db.session, default_error_message=u'Failed to delete todo.'):
            TodoService.delete(todo.id)
