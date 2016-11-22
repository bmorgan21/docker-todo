from ct_core_api.api.app.factory import create_api_app

import config


def create_app(import_name, *args, **kwargs):
    kwargs.setdefault('config', config)

    app = create_api_app(import_name, *args, **kwargs)

    from app import logging
    logging.init_app(app)

    from app import extensions
    extensions.init_app(app)

    from app import modules
    modules.init_app(app)

    from app import commands
    commands.init_app(app)

    return app
