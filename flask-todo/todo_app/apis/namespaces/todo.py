from flask import request
from flask_restplus import Namespace, Resource, fields

from todo_app.services import todo as todo_svc
from todo_app.models import db


ns = Namespace('todos', description='TODO operations')

todo = ns.model('Todo', {
    'id': fields.Integer(readOnly=True, description='The task unique identifier'),
    'title': fields.String(required=True, description='The task details', attribute='name'),
    'completed': fields.Boolean(description='Mark whether the task is complete', attribute='is_complete')
})


@ns.route('/')
class TodoList(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''
    @ns.doc('list_todos')
    @ns.marshal_list_with(todo)
    def get(self):
        '''List all tasks'''
        return todo_svc.get_all()

    @ns.doc('create_todo')
    @ns.expect(todo)
    @ns.marshal_with(todo, code=201)
    def post(self):
        '''Create a new task'''
        todo = todo_svc.create_from_dict(request.json)

        db.session.commit()

        return todo, 201


@ns.route('/<int:id>')
@ns.response(404, 'Todo not found')
@ns.param('id', 'The task identifier')
class Todo(Resource):
    '''Show a single todo item and lets you delete them'''
    @ns.doc('get_todo')
    @ns.marshal_with(todo)
    def get(self, id):
        '''Fetch a given resource'''
        return todo_svc.get(id)

    @ns.doc('delete_todo')
    @ns.response(204, 'Todo deleted')
    def delete(self, id):
        '''Delete a task given its identifier'''
        todo_svc.delete(id)

        db.session.commit()

        return '', 204

    @ns.expect(todo)
    @ns.marshal_with(todo)
    def put(self, id):
        '''Update a task given its identifier'''
        todo = todo_svc.update(id, request.json)

        db.session.commit()

        return todo, 204
