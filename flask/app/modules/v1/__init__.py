from flask import Blueprint

from app.extensions.api_ext import api


def init_app(app):
    from app.modules.v1.error_handlers import register_handlers
    from app.modules.v1 import todo_resources, token_resources, user_resources

    register_handlers(api)
    api.add_namespace(todo_resources.api)
    api.add_namespace(token_resources.api)
    api.add_namespace(user_resources.api)

    api_v1_blueprint = Blueprint('api-v1', __name__, url_prefix='/v1')

    api.init_app(api_v1_blueprint)
    app.register_blueprint(api_v1_blueprint)
