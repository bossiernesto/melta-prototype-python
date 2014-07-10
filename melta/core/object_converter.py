from abc import ABCMeta, abstractmethod
from .basicmodel import AtomicObject, AggregationObject
from .random import generate_object_name
from melta.utils.utils import listify, is_python_instance

#TODO: make tests and complete

class GenericConverter(object):
    """
    Abstract class with the contract of the methods that it's subclasses should implement
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def to_melta_object(self, python_object, alternate_name=None, transactions=False):
        raise NotImplementedError('Should be implemented in sublcass')

    @abstractmethod
    def to_object(self, python_object):
        raise NotImplementedError('Should be implemented in subclass')

    def name_by_param_or_type(self, python_object, name=None):
        return name or generate_object_name(type(object))


class DictionaryConverter(GenericConverter):
    def to_melta_object(self, python_object, alternate_name=None, transactions=False):
        name = self.name_by_param_or_type(python_object, alternate_name)
        return AggregationObject(name, **python_object)

    def to_object(self, melta_object):
        pass


class InstanceConverter(GenericConverter):
    def to_melta_object(self, python_object, alternate_name=None, transactions=False):
        name = python_object.__class__
        #TODO

    def to_object(self, melta_object):
        pass


class StringConverter(GenericConverter):
    def to_melta_object(self, python_object, alternate_name=None, transactions=False):
        name = self.name_by_param_or_type(python_object, alternate_name)
        return AtomicObject(name, python_object)

    def to_object(self, melta_object):
        return melta_object.value


class IntegerConverter(GenericConverter):
    def to_melta_object(self, python_object, alternate_name=None, transactions=False):
        name = self.name_by_param_or_type(python_object, alternate_name)
        return AtomicObject(name, python_object)

    def to_object(self, melta_object):
        return melta_object.value


class ListConverter(GenericConverter):
    def to_melta_object(self, python_object, alternate_name=None, transactions=False):
        elements_meltized = self.convert_elements(object)
        name = self.name_by_param_or_type(object, alternate_name)
        return AggregationObject(name, **elements_meltized)

    @listify
    def convert_elements(self, python_object):
        for element in python_object:
            if is_python_instance(element):
                yield InstanceConverter().to_melta_object(element)
            else:
                yield OBJECT_CONVERSORS[type(python_object)]().to_melta_object(element)

    def to_object(self, melta_object):
        pass


OBJECT_CONVERSORS = {'dict': DictionaryConverter, 'instance': InstanceConverter, 'str': StringConverter,
                     'int': IntegerConverter, 'list': ListConverter}


class MeltaObjectConverter(object):
    def __init__(self):
        self.conversor = None

    def to_melta_object(self, python_object, alternate_name=None, transactions=False):
        converter = InstanceConverter() if is_python_instance(python_object) else OBJECT_CONVERSORS[
            type(python_object)]()
        converter.to_melta_object(python_object, alternate_name, transactions)

    def to_object(self, melta_result_set):
        pass
