# TODO: Consider moving this into `ct-core-db`
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
    def _apply_contraints(cls, q, **kwargs):
        for k, v in kwargs.items():
            if isinstance(v, (list, tuple)):
                q = q.filter(getattr(cls.__model__, k).in_(v))
            else:
                q = q.filter(getattr(cls.__model__, k) == v)

        return q

    @classmethod
    def create(cls, **kwargs):
        return cls.__model__(**kwargs)

    @classmethod
    def get(cls, *args, **kwargs):
        raise_not_found = kwargs.pop('raise_not_found', True)

        q = cls.__model__.query
        if len(args) == 1:
            q = q.filter(cls.__model__.id == args[0])

        q = cls._apply_contraints(q, **kwargs)

        if raise_not_found:
            return q.one()
        return q.first()

    @classmethod
    def get_many(cls, offset=None, limit=None, **kwargs):
        q = cls.__model__.query

        q = cls._apply_contraints(q, **kwargs)

        cls._apply_limit_offset(q, limit, offset)

        return q.all()

    @classmethod
    def delete(cls, id_):
        # first make sure it exists, before we delete it
        if not isinstance(id_, cls.__model__):
            cls.get(id_)

        cls.__model__.query.filter(cls.__model__.id == id_).delete()

    @classmethod
    def update(cls, id_, d):
        if isinstance(id_, cls.__model__):
            obj = id_
        else:
            obj = cls.get(id_)

        for k, v in d.items():
            setattr(obj, k, v)

        return obj
