from ct_core_api.api.common import api_helpers as ah

from app.extensions.api_ext import api_v1_0


def init_app(app):
    from app.modules import register_api_error_handlers
    ah.register_api_resources(app, api_v1_0, __path__, __name__, url_prefix='')
    register_api_error_handlers(api_v1_0)
