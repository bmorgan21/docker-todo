from flask import Blueprint
from flask_principal import PermissionDenied
from flask_restplus import Api
from validation21.exception import ValidationException
from sqlalchemy.orm.exc import NoResultFound

bp = Blueprint('api', __name__)
api = Api(bp, title='Todo API',
          doc='/doc/',
          validate=True)

###
# Register namespaces
##
from todo_app.apis.namespaces import todo as namespace_todo

api.add_namespace(namespace_todo.ns)


###
# Register Error Handlers
##
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
