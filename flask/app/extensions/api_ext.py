from ct_core_api.api.core.api import API


authorizations = {
    'token': {
        'type': 'apiKey',
        'in': 'query',
        'name': 'token'
    },
    'basic': {
        'type': 'basic',
        'in': 'header',
        'name': 'Authorization'
    }
}


def _create_api(version):
    return API(
        version=version,
        title=u'Todo Docker',
        description=u'The Todo Docker Application API',
        authorizations=authorizations,
        security=['token', 'basic'])

api_v1_0 = _create_api('1.0')
api_v1_1 = _create_api('1.1')


def init_app(app):
    app.register_extension(api_v1_0, 'api-v1.0')
    app.register_extension(api_v1_1, 'api-v1.1')
