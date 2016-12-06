import logging

from flask_login import current_user, login_required

from ct_core_api.api.core import response
from ct_core_api.api.core.namespace import APINamespace
from ct_core_api.api.core.resource import APIResource
from ct_core_api.api.core.parameters import Parameters
from ct_core_api.core.database import db

from app.extensions.principal_ext import admin_permission
from app.schemas import user_schemas
from app.services.user_service import UserService

_logger = logging.getLogger(__name__)

api = APINamespace('users', description="Users")


@api.route('/')
class UserCollectionResource(APIResource):
    class PostUserParameters(Parameters, user_schemas.UserSchema):
        pass

    @api.parameters(PostUserParameters(), locations=['json'])
    @api.response(user_schemas.UserSchema())
    @api.response(code=response.Forbidden.code)
    @api.response(code=response.Conflict.code)
    def post(self, args):
        """Create a new User."""
        with api.commit_or_abort(db.session, default_error_message=u"Failed to create a new User."):
            new_user = UserService.create(**args)
            db.session.add(new_user)
        return new_user


@api.route('/<int:id>')
@api.resolve_object_by_find('user', UserService.get)
@api.response(code=response.Forbidden.code, description=u"Permission Denied.")
@api.response(code=response.NotFound.code, description=u"User not found.")
class UserResource(APIResource):
    class PatchUserParameters(Parameters, user_schemas.UserSchema):
        pass

    def _check_permission(self, user):
        if not (admin_permission.can() or current_user.id == user.id):
            response.abort(response.Forbidden)

    @login_required
    @api.response(user_schemas.UserSchema())
    def get(self, user):
        """Get user details by id."""
        self._check_permission(user)
        return user

    @login_required
    @api.parameters(PatchUserParameters(), locations=['json'])
    @api.response(user_schemas.UserSchema())
    @api.response(code=response.Conflict.code)
    def patch(self, args, user):
        """Patch user details by id."""
        self._check_permission(user)

        with api.commit_or_abort(db.session, default_error_message=u'Failed to update user details.'):
            UserService.update(user, args)
        return user
