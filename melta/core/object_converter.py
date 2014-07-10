from abc import ABCMeta, abstractmethod

#TODO: make tests and complete

OBJECT_CONVERSORS = {'dict': DictionaryConversor, 'instance': InstanceConversor, 'str': StringConversor,
                     'int': IntegerConversor, 'list': ListConversor}


class MeltaObjectConverter(object):
    def __init__(self):
        self.conversor = None

    def to_melta_object(self, object, alternate_name=None, transactions=False):
        pass

    def to_object(self, melta_object):
        pass


class GenericConversor(object):
    """

    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def to_melta_object(self, object, alternate_name=None, transactions=False):
        raise NotImplementedError('Should be implemented in sublcass')

    @abstractmethod
    def to_object(self, melta_object):
        raise NotImplementedError('Should be implemented in subclass')