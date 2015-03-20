import weakref
import types

INSTANCE_TYPE = 'instance'


def istypeof(obj, type_class):
    return type(obj) == type_class


def is_melta_instance_type(melta_object):
    return melta_object.metadata.type == INSTANCE_TYPE

class AUX:
    pass


aux = AUX()
WeakRefType = type(weakref.ref(aux))
WeakProxyType = type(weakref.proxy(aux))
