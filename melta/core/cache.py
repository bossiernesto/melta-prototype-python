__author__ = 'ernesto'

from weakref import WeakValueDictionary
from melta.core.basicmodel import MeltaBaseObject

class MeltaCache(WeakValueDictionary):

    def add_object(self, melta_object):
        if isinstance(melta_object, MeltaBaseObject):
            self.__setitem__(melta_object.id,melta_object)