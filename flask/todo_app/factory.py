from ct_core_api.api.app.factory import create_api_app

import config


def create_app(import_name, *args, **kwargs):
    kwargs.setdefault('config', config)

    app = create_api_app(import_name, *args, **kwargs)

    from todo_app import logging
    logging.init_app(app)

    from todo_app import extensions
    extensions.init_app(app)

    from todo_app import modules
    modules.init_app(app)

    from todo_app import commands
    commands.init_app(app)

    return app
