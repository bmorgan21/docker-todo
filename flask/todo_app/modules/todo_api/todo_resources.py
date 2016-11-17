import logging

from ct_core_api.api.core.namespace import APINamespace
from ct_core_api.api.core.resource import APIResource

from todo_app.services.todo_service import TodoService

_logger = logging.getLogger(__name__)

api = APINamespace('todos', description="TODOs")


@api.route('/')
class TodoCollectionResource(APIResource):
    pass

# FIXME: Convert
from flask import request, abort
from flask_login import login_required, current_user
from flask_restplus import Namespace, Resource, fields

ns = Namespace('todos', description='TODO operations')

todo = ns.model('Todo', {
    'id': fields.Integer(readOnly=True, description='The task unique identifier'),
    'title': fields.String(description='The task details', attribute='name'),
    'completed': fields.Boolean(description='Mark whether the task is complete', attribute='is_complete')
})


def transform_data(d):
    result = {}

    map = {
        'title': 'name',
        'completed': 'is_complete'
    }

    for k, v in d.items():
        if k in map:
            result[map[k]] = v

    return result


@ns.route('/')
class TodoList(Resource):
    """Shows a list of all todos, and lets you POST to add new tasks"""
    @login_required
    @ns.doc('list_todos')
    @ns.marshal_list_with(todo)
    def get(self):
        """List all tasks"""
        return TodoService.get_many(user_id=current_user.id)

    @login_required
    @ns.doc('create_todo')
    @ns.expect(todo)
    @ns.marshal_with(todo, code=201)
    def post(self):
        """Create a new task"""

        data = transform_data(request.json)
        data['user_id'] = current_user.id
        todo = TodoService.create(**data)

        db.session.add(todo)
        db.session.commit()

        return todo, 201


@ns.route('/<int:id>')
@ns.response(404, 'Todo not found')
@ns.param('id', 'The task identifier')
class Todo(Resource):
    def _get_todo_for_user_id(self, id, user_id):
        todo = TodoService.get(id)

        if not admin_permission.can() and todo.user_id != current_user.id:
            abort(403)

        return todo

    '''Show a single todo item and lets you delete them'''
    @login_required
    @ns.doc('get_todo')
    @ns.marshal_with(todo)
    def get(self, id):
        """Fetch a given resource"""
        return self._get_todo_for_user_id(id, current_user.id)

    @login_required
    @ns.doc('delete_todo')
    @ns.response(204, 'Todo deleted')
    def delete(self, id):
        """Delete a task given its identifier"""
        self._get_todo_for_user_id(id, current_user.id)

        TodoService.delete(id)

        db.session.commit()

        return '', 204

    @login_required
    @ns.expect(todo)
    @ns.marshal_with(todo)
    def put(self, id):
        """Update a task given its identifier"""
        self._get_todo_for_user_id(id, current_user.id)

        todo = TodoService.update(id, transform_data(request.json))

        db.session.commit()

        return todo
