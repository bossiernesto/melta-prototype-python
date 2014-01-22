from .utils.random import generate_object_id, generate_object_name
from .exceptions.exceptions import NotFoundMeltaObject


class MeltaBaseObject(object):
    def __init__(self, melta_instance_name=None, *args, **kwargs):
        self.id = generate_object_id()
        self.instance_name = melta_instance_name or self.generate_name()

    def generate_name(self):
        return generate_object_name(self.__class__.__name__)


class AggregationObject(MeltaBaseObject):
    def __init__(self, melta_instance_name=None, *args, **kwargs):
        super(AggregationObject, self).__init__(melta_instance_name=melta_instance_name, *args, **kwargs)
        self._atomic_attributes = []
        if kwargs:
            self.set_attrbutes(**kwargs)

    def set_attrbutes(self, **kwargs):
        for name in kwargs:
            self._atomic_attributes.append(AtomicObject(name, kwargs[name]))

    def _find_atomic_attribute_(self, name):
        value = [atomic.value for atomic in self._atomic_attributes if atomic.instance_name == name][0]
        if not value:
            raise NotFoundMeltaObject
        return value

    def __getattribute__(self, name):
        try:
            return super(AggregationObject, self).__getattribute__(name)
        except AttributeError:
            return self._find_atomic_attribute_(name)


class AtomicObject(MeltaBaseObject):
    def __init__(self, melta_instance_name=None, value=None):
        super(AtomicObject, self).__init__(melta_instance_name)
        self.value = value


