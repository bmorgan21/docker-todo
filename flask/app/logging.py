from __future__ import absolute_import

import logging  # noqa


def init_app(app):
    # TODO: Enable debug logging for certain third-party libs (optional)
    if app.debug:
        pass  # logging.getLogger('flask_oauthlib').setLevel(logging.DEBUG)
