from ct_core_api.api.core.schema import APISchema, ma


# USER: Consider using `ModelSchema` here instead
class UserSchema(APISchema):
    id = ma.Str(dump_only=True)
    first_name = ma.Str()
    last_name = ma.Str()
    email = ma.Email()
