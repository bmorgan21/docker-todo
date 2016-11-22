from model_manager import ProxyManager


class Service(object):
    __metaclass__ = ProxyManager
    __manager__ = None
