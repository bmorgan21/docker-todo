from ct_core_api.api.core.api import API

todo_api = API(version='1.0', title=u'TODO', description=u'The TODO Application API')


def init_app(app):
    app.register_extension(todo_api, 'todo-api-v1')
