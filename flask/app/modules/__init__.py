from app.modules import v1


def init_app(app):
    for module in (v1,):
        module.init_app(app)
