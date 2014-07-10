class MeltaException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class AtomicObjectInvalidArgumentsException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class NotFoundMeltaObject(MeltaException):
    def __init__(self, *args, **kwargs):
        MeltaException.__init__(self, *args, **kwargs)


class NotFoundMeltaObject(MeltaException):
    def __init__(self, *args, **kwargs):
        MeltaException.__init__(self, *args, **kwargs)
