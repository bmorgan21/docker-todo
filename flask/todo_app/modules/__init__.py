from todo_app.modules import admin, auth, todo, todo_api, user


def init_app(app):
    for module in (admin, auth, todo, todo_api, user):
        module.init_app(app)
