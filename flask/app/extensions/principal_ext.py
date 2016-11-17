from flask_principal import Principal

principal = Principal()


def init_app(app):
    principal.init_app(app)
    app.register_extension(principal, 'flask-principal')
