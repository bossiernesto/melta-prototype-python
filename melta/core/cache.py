from weakref import WeakValueDictionary
from melta.core.basicmodel import MeltaBaseObject

#TODO: change this to a real cache
class MeltaCache(WeakValueDictionary):
    """
    Melta cache keeps a
    """

    def add_object(self, melta_object, original_object=None):
        if isinstance(melta_object, MeltaBaseObject):
            self.__setitem__(melta_object.get_id(), MeltaCacheObject(melta_object, original_object))


class MeltaCacheObject(object):
    def __init__(self, melta_object, python_object):
        self.python_object = python_object
        self.melta_object = melta_object

    def update_python_object(self):
        pass