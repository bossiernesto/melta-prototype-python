from .random import generate_object_id, generate_object_name


class AtomicObject(object):
    def __init__(self, melta_instance_name=None, *args, **kwargs):
        self.id = generate_object_id()
        print(self.generate_name())
        self.instance_name = melta_instance_name or self.generate_name()
        if kwargs:
            self.set_attrbutes(**kwargs)

    def set_attrbutes(self, **kwargs):
        for name in kwargs:
            setattr(self, name, kwargs[name])

    def generate_name(self):
        return generate_object_name(self.__class__.__name__)