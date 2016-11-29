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

api = API(version='1.0', title=u'Todo Docker', description=u'The Todo Docker Application API', authorizations=authorizations, security=['token', 'basic'])


def init_app(app):
    app.register_extension(api, 'api-v1')
