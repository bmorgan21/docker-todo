from app.commands import shell_cmd


def init_app(app):
    for cmd in (shell_cmd,):
        cmd.init_app(app)
