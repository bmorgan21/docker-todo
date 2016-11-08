class ModelManager(object):

    @classmethod
    def create(cls, **kwargs):
        raise NotImplementedError()

    @classmethod
    def get(cls, *args, **kwargs):
        raise NotImplementedError()

    @classmethod
    def get_many(cls, offset=None, limit=None, **kwargs):
        raise NotImplementedError()

    @classmethod
    def delete(cls, id_):
        raise NotImplementedError()

    @classmethod
    def update(cls, id_, d):
        raise NotImplementedError()


class SqlAlchemyModelManager(ModelManager):
    __model__ = None

    @staticmethod
    def _apply_limit_offset(q, limit, offset):
        if offset is not None:
            q = q.offset(offset)

        if limit is not None:
            q = q.limit(limit)

        return q

    @classmethod
    def create(cls, **kwargs):
        return cls.__model__(**kwargs)

    @classmethod
    def get(cls, *args, **kwargs):
        raise_not_found = kwargs.pop('raise_not_found', True)

        q = cls.__model__.query
        if len(args) == 1:
            q = q.filter(cls.__model__.id_ == args[0])

        for k, v in kwargs.items():
            q = q.filter(getattr(cls.__model__, k) == v)

        if raise_not_found:
            return q.one()
        return q.first()

    @classmethod
    def get_many(cls, offset=None, limit=None, **kwargs):
        q = cls.__model__.query
        for k, v in kwargs.items():
            q = q.filter(getattr(cls.__model__, k) == v)

        cls._apply_limit_offset(q, limit, offset)

        return q.all()

    @classmethod
    def delete(cls, id_):
        # first make sure it exists, before we delete it
        if not isinstance(id_, cls.__model__):
            cls.get(id_)

        cls.__model__.query.filter(cls.__model__.id_ == id_).delete()

    @classmethod
    def update(cls, id_, d):
        if isinstance(id_, cls.__model__):
            obj = id_
        else:
            obj = cls.get(id_)

        for k, v in d.items():
            setattr(obj, k, v)

        return obj


from todo_app.models import (
    Role,
    Todo,
    User
)


class TodoManager(SqlAlchemyModelManager):
    __model__ = Todo


class UserManager(SqlAlchemyModelManager):
    __model__ = User

    @staticmethod
    def add_role(user_id, name):
        return RoleManager.create(user_id=user_id, name=name)

    @staticmethod
    def get_roles(user_id):
        return RoleManager.get_many(user_id=user_id)


class RoleManager(SqlAlchemyModelManager):
    __model__ = Role
