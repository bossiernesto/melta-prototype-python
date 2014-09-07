from abc import ABCMeta, abstractmethod
from .basicmodel import AtomicObject, AggregationObject
from .random import generate_object_name
from melta.utils.utils import listify, is_python_instance, getAttributes, get_python_type_name
from .melta_types import INSTANCE_TYPE

#TODO: make tests and complete


class GenericConverter(object):
    """
    Abstract class with the contract of the methods that it's subclasses should implement
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def to_melta_object(self, python_object, alternate_name=None):
        raise NotImplementedError('Should be implemented in sublcass')

    @abstractmethod
    def to_object(self, melta_object):
        raise NotImplementedError('Should be implemented in subclass')

    def name_by_param_or_type(self, python_object, name=None):
        return name or generate_object_name(type(object))

    @listify
    def _aggregated_melta_object_to_list(self, melta_object):
        for melta_member in melta_object.get_attributes():
            yield OBJECT_CONVERSORS[melta_member.get_data_type()]().to_object(melta_member)

    def _aggregated_melta_object_to_dict(self, melta_object):
        auxiliary_dictionary = {}
        for melta_member in melta_object.get_attributes():
            python_object = OBJECT_CONVERSORS[melta_member.get_data_type()]().to_object(melta_member)
            auxiliary_dictionary[melta_member.instance_name] = python_object
        return auxiliary_dictionary


class PrimitiveConverter(GenericConverter):
    def to_melta_object(self, python_object, alternate_name=None):
        name = self.name_by_param_or_type(python_object, alternate_name)
        return AtomicObject(name, python_object)

    def to_object(self, melta_object):
        return melta_object.value


StringConverter = PrimitiveConverter
IntegerConverter = PrimitiveConverter
FloatConverter = PrimitiveConverter

#TODO: Remove this NullConverter when all types have a protocol of Converter implemented.
class NullConverter(GenericConverter):
    def to_melta_object(self, python_object, alternate_name=None):
        return AtomicObject(generate_object_name(python_object), 43)

    def to_object(self, melta_object):
        pass


class DictionaryConverter(GenericConverter):
    def to_melta_object(self, python_object, alternate_name=None):
        name = self.name_by_param_or_type(python_object, alternate_name)
        object_type = get_python_type_name(python_object)
        return AggregationObject(name, object_type, **python_object)

    def to_object(self, melta_object):
        return self._aggregated_melta_object_to_dict(melta_object)


class InstanceConverter(GenericConverter):
    def to_melta_object(self, python_object, alternate_name=None):
        klass_name = python_object.__class__
        melta_objects = self.meltize_instance_attributes(python_object)
        return AggregationObject(klass_name, INSTANCE_TYPE, *melta_objects)

    @listify
    def meltize_instance_attributes(self, python_object):
        for attribute_name in getAttributes(python_object):
            value = getattr(python_object, attribute_name)
            yield MeltaObjectConverter().to_melta_object(value, attribute_name)

    def to_object(self, melta_object):
        attributes = self._aggregated_melta_object_to_dict(melta_object)
        instance = melta_object.metadata.original_class()
        for k, v in attributes.items():
            setattr(instance, k, v)
        return instance


class ListConverter(GenericConverter):
    def to_melta_object(self, python_object, alternate_name=None):
        elements_meltized = self.convert_elements(python_object)
        object_type = get_python_type_name(python_object)
        name = self.name_by_param_or_type(object, alternate_name)
        return AggregationObject(name, object_type, *elements_meltized)

    @listify
    def convert_elements(self, python_object):
        for element in python_object:
            if is_python_instance(element):
                yield InstanceConverter().to_melta_object(element)
            else:
                yield OBJECT_CONVERSORS[get_python_type_name(element)]().to_melta_object(element)

    def to_object(self, melta_object):
        return self._aggregated_melta_object_to_list(melta_object)


OBJECT_CONVERSORS = {'dict': DictionaryConverter, INSTANCE_TYPE: InstanceConverter, 'str': StringConverter,
                     'int': IntegerConverter, 'float': FloatConverter, 'list': ListConverter, 'method': NullConverter}


class MeltaObjectConverter(object):
    def to_melta_object(self, python_object, alternate_name=None):
        converter = InstanceConverter() if is_python_instance(python_object) else OBJECT_CONVERSORS[
            get_python_type_name(python_object)]()
        return converter.to_melta_object(python_object, alternate_name)

    def to_object(self, melta_object):
        return OBJECT_CONVERSORS[melta_object.get_data_type()]().to_object(melta_object)
