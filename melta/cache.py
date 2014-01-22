__author__ = 'ernesto'

from weakref import WeakValueDictionary
from melta.basicmodel import MeltaBaseObject

#TODO: change this to a real cache
class MeltaCache(WeakValueDictionary):

    def add_object(self, melta_object):
        if isinstance(melta_object, MeltaBaseObject):
            self.__setitem__(melta_object._id,melta_object)