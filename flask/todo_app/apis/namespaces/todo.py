from flask import request, abort
from flask_login import login_required, current_user
from flask_restplus import Namespace, Resource, fields

from todo_app.services import todo as todo_svc
from todo_app.models import db
from todo_app.extensions.principal import admin_permission


ns = Namespace('todos', description='TODO operations')

todo = ns.model('Todo', {
    'id': fields.Integer(readOnly=True, description='The task unique identifier'),
    'title': fields.String(description='The task details', attribute='name'),
    'completed': fields.Boolean(description='Mark whether the task is complete', attribute='is_complete')
})


@ns.route('/')
class TodoList(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''
    @login_required
    @ns.doc('list_todos')
    @ns.marshal_list_with(todo)
    def get(self):
        '''List all tasks'''
        return todo_svc.get_all_for_user_id(current_user.id)

    @login_required
    @ns.doc('create_todo')
    @ns.expect(todo)
    @ns.marshal_with(todo, code=201)
    def post(self):
        '''Create a new task'''

        data = {'title': request.json['title'],
                'completed': request.json['completed'],
                'user_id': current_user.id}
        todo = todo_svc.create_from_dict(data)

        db.session.commit()

        return todo, 201


@ns.route('/<int:id>')
@ns.response(404, 'Todo not found')
@ns.param('id', 'The task identifier')
class Todo(Resource):
    def _get_todo_for_user_id(self, id, user_id):
        todo = todo_svc.get(id)

        if not todo:
            abort(404)

        if not admin_permission.can() and str(todo.user_id) != current_user.id:
            abort(403)

        return todo

    '''Show a single todo item and lets you delete them'''
    @login_required
    @ns.doc('get_todo')
    @ns.marshal_with(todo)
    def get(self, id):
        '''Fetch a given resource'''
        return self._get_todo_for_user_id(id, current_user.id)

    @login_required
    @ns.doc('delete_todo')
    @ns.response(204, 'Todo deleted')
    def delete(self, id):
        '''Delete a task given its identifier'''
        self._get_todo_for_user_id(id, current_user.id)

        todo_svc.delete(id)

        db.session.commit()

        return '', 204

    @login_required
    @ns.expect(todo)
    @ns.marshal_with(todo)
    def put(self, id):
        '''Update a task given its identifier'''
        self._get_todo_for_user_id(id, current_user.id)

        todo = todo_svc.update(id, request.json)

        db.session.commit()

        return todo
