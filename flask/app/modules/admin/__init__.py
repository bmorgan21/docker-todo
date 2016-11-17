def init_app(app):
    from app.modules.admin import admin_views
    admin_views.admin.init_app(app)
