from ct_core_api.api.core.schema import APISchema, ma


class TokenSchema(APISchema):
    token = ma.Str()
