def init_app(app):
    # Make additional context available to the shell/shell2 commands
    @app.shell_context_processor
    def shell_cmd_context():
        from app import models
        return {'m': models}
