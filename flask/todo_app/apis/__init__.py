from flask import Blueprint
from flask_restplus import Api

bp = Blueprint('api', __name__)
api = Api(bp, title='Todo API',
          doc='/doc/',
          validate=True)

###
# Register namespaces
##
from todo_app.apis.namespaces import todo as namespace_todo

api.add_namespace(namespace_todo.ns)
