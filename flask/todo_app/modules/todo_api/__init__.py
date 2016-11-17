from flask import Blueprint

from todo_app.extensions.todo_api_ext import todo_api


def init_app(app):
    from todo_app.modules.todo_api import todo_resources
    todo_api.add_namespace(todo_resources.api)

    api_v1_blueprint = Blueprint('todo-api-v1', __name__, url_prefix='/todo/api/v1')
    todo_api.init_app(api_v1_blueprint)
    app.register_blueprint(api_v1_blueprint)
