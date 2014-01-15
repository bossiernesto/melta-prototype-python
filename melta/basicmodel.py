from .random import generate_object_id, generate_object_name


class MeltaBaseObject(object):
    def __init__(self, melta_instance_name=None, *args, **kwargs):
        self.id = generate_object_id()
        self.instance_name = melta_instance_name or self.generate_name()

    def generate_name(self):
        return generate_object_name(self.__class__.__name__)


class AggregationObject(MeltaBaseObject):
    def __init__(self, melta_instance_name=None, *args, **kwargs):
        super(AggregationObject, self).__init__(melta_instance_name=melta_instance_name, *args, **kwargs)
        if kwargs:
            self.set_attrbutes(**kwargs)

    def set_attrbutes(self, **kwargs):
        for name in kwargs:
            setattr(self, name, kwargs[name])

    def __getattribute__(self, name):
        attr_value = super(AggregationObject, self).__getattribute__(name)
        return attr_value


class AtomicObject(MeltaBaseObject):
    def __init__(self, melta_instance_name=None, *args, **kwargs):
        super(AtomicObject, self).__init__(melta_instance_name, *args, **kwargs)
        self.check_one_argument_restriction(*args)
        self.assign_arguments(*args)

    def check_one_argument_restriction(self, *arguments):
        if len(arguments) > 1:
            raise AtomicObjectInvalidArgumentsException('You can only input a single value to an Atomic Object, trying to assign {0} values'.format(
                len(arguments)))

    def assign_arguments(self, *arguments):
        if not arguments:
            self.value = None
            return
        self.value = arguments[0]


class AtomicObjectInvalidArgumentsException(Exception):
    pass