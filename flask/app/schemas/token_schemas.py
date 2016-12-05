from ct_core_api.api.core.schema import APISchema, ma


class TokenSchema(APISchema):
    user_id = ma.Int()
    token = ma.Str()
