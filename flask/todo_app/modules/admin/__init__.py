def init_app(app):
    from todo_app.modules.admin import admin_views
    admin_views.admin.init_app(app)
