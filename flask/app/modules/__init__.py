from app.modules import api_v1_0, api_v1_1


def init_app(app):
    for module in (api_v1_0, api_v1_1):
        module.init_app(app)


# TODO: Move `register_api_error_handlers` to `ct-core-api` or some shared module?
def register_api_error_handlers(api):
    from flask_principal import PermissionDenied
    from sqlalchemy.orm.exc import NoResultFound
    from validation21 import ValidationException

    @api.errorhandler(ValidationException)
    def validation_exception_handler(e):
        if e.error_dict:
            errors = {}
            for k, v in e.error_dict:
                errors[v.field] = e.message
        else:
            errors = {e.field: e.message}

        return {'message': 'Validation failed', 'errors': errors}, 400

    @api.errorhandler(PermissionDenied)
    def permission_denied_handler(e):
        return {'message': str(e.message)}, 403

    @api.errorhandler(NoResultFound)
    def no_result_found_handler(e):
        return {'message': 'Not Found'}, 404
