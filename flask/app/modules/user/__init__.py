def init_app(app):
    from app.modules.user import user_views
    app.register_blueprint(user_views.bp, url_prefix='/user')