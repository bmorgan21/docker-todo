from flask_cors import CORS

cross_origin_resource_sharing = CORS(supports_credentials=True)


def init_app(app):
    cross_origin_resource_sharing.init_app(app)
    app.register_extension(cross_origin_resource_sharing, 'flask-cors')
