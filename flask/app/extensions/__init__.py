from app.extensions import login_manager_ext, mail_ext, principal_ext, api_ext, cors_ext


def init_app(app):
    for module in (login_manager_ext, principal_ext, mail_ext, api_ext, cors_ext):
        module.init_app(app)
