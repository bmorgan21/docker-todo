def init_app(app):
    from app.modules.todo import todo_views
    app.register_blueprint(todo_views.bp, url_prefix='/todo')