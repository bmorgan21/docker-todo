class ProxyManager(type):
    def __getattr__(cls, key):
        if cls.__manager__:
            return getattr(cls.__manager__, key)
        raise AttributeError(key)


class Service(object):
    __metaclass__ = ProxyManager
    __manager__ = None
