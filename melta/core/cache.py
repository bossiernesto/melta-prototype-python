from weakref import WeakValueDictionary
from melta.core.basicmodel import MeltaBaseObject

#TODO: change this to a real cache
class MeltaCache(WeakValueDictionary):
    """
    Melta cache is a bookkeeping mechanism of MeltaCacheObjects associated with the melta_object id, the CacheObjects
    have the original python object in the enviroment and in case of querying it'll consult this very cache.
    Probably the best idea is to implement a LRU cache for now.
    """

    def add_object(self, melta_object, original_object=None):
        if isinstance(melta_object, MeltaBaseObject):
            self.__setitem__(melta_object.get_id(), MeltaCacheObject(melta_object, original_object))


class MeltaCacheObject(object):
    def __init__(self, melta_object, python_object):
        self.python_object = python_object
        self.melta_object = melta_object
        self.access_counter = 0