from flask_principal import PermissionDenied
from sqlalchemy.orm.exc import NoResultFound
from validation21 import ValidationException


def register_handlers(api):
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
