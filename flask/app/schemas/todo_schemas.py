from ct_core_api.api.core.schema import APISchema, ma


# TODO: Consider using `ModelSchema` here instead
class TodoSchema(APISchema):
    id = ma.Str(dump_only=True)
    title = ma.Str(attribute='name', description='foo')
    is_complete = ma.Boolean(default=False)
