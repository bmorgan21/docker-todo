class ModelManager(object):
    __model__ = None

    @classmethod
    def create(cls, **kwargs):
        return cls.__model__(**kwargs)

    @classmethod
    def get(cls, *args, **kwargs):
        q = cls.__model__.query
        if len(args) == 1:
            q = q.filter(cls.__model__.id == args[0])

        for k, v in kwargs.items():
            q = q.filter(getattr(cls.__model__, k) == v)

        return q.one()

    @classmethod
    def get_many(cls, offset=None, limit=None, **kwargs):
        q = cls.__model__.query
        for k, v in kwargs.items():
            q.filter(getattr(cls.__model__, k) == v)

        if offset is not None:
            q = q.offset(offset)

        if limit is not None:
            q = q.limit(limit)

        return q.all()

    @classmethod
    def delete(cls, id):
        # first make sure it exists, before we delete it
        if not isinstance(id, cls.__model__):
            cls.get(id)

        cls.__model__.query.filter(cls.__model__.id == id).delete()

    @classmethod
    def update(cls, id, d):
        if isinstance(id, cls.__model__):
            obj = id
        else:
            obj = cls.get(id)

        for k, v in d.items():
            setattr(obj, k, v)

        return obj


from checkout.models import (
    Role,
    User
)


class UserManager(ModelManager):
    __model__ = User

    @staticmethod
    def add_role(user_id, name):
        return Role(user_id=user_id, name=name)

    @staticmethod
    def get_roles(user_id):
        return Role.query.filter(Role.user_id == user_id).all()
