from todo_app.extensions import mail_ext, principal_ext, todo_api_ext


def init_app(app):
    for module in (principal_ext, mail_ext, todo_api_ext):
        module.init_app(app)
