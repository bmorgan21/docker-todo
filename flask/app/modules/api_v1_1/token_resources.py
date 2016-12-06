import logging

from ct_core_api.api.core import response
from ct_core_api.api.core.namespace import APINamespace
from ct_core_api.api.core.resource import APIResource
from ct_core_api.api.core.schema import ma
from ct_core_api.api.core.parameters import Parameters
from ct_core_api.core.database import db

from app.schemas import token_schemas
from app.services.user_service import UserService
from app.extensions.login_manager_ext import login_user

_logger = logging.getLogger(__name__)

api = APINamespace('tokens', description="Tokens")


@api.route('/')
class TokenCollectionResource(APIResource):
    class PostTokenParameters(Parameters):
        email = ma.Email()
        password = ma.Str()

    @api.parameters(PostTokenParameters(), locations=['json'])
    @api.response(token_schemas.TokenSchema())
    @api.response(code=response.Unauthorized.code)
    def post(self, args):
        """Create a new Token."""
        user = UserService.get(email=args['email'], raise_not_found=False)

        if not user:
            response.abort(response.Unauthorized.code)

        verified = False
        if UserService.check_password(user.password, args['password']):
            verified = True
        elif UserService.check_password(user.temp_password, args['password']):
            verified = True
            # these are only good once
            UserService.set_password(user, None, attr='temp_password')

        if verified:
            token = login_user(user)  # user.tick is bumped with each login

            db.session.commit()
            return {'token': token, 'user_id': user.id}
        else:
            response.abort(response.Unauthorized.code)
