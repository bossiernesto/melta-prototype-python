from .random import generate_object_id, generate_object_name
from melta.exceptions.exceptions import MeltaException, NotFoundMeltaObject
from .metadata import MetadataObject
from .melta_types import INSTANCE_TYPE
from melta.transactions.transactional import Transaction


class MeltaBaseObject(Transaction, object):
    def __init__(self, melta_instance_name=None, *args, **kwargs):
        self._id = generate_object_id()
        self.instance_name = melta_instance_name or self.generate_name()
        self.metadata = MetadataObject(self)

    def get_id(self):
        return self._id

    def get_data_type(self):
        raise NotImplementedError('Should be implemented in subclass.')

    def generate_name(self):
        return generate_object_name(self.__class__.__name__)

    def validate_base_object(self, base_object):
        if not isinstance(base_object, self.__class__):
            raise MeltaException

    def added_to_schema(self, schema):
        self.metadata.schema = schema

    def remove_reference(self, reference):
        self.metadata.remove_reference(reference)

    def get_metadata(self):
        return self.metadata

    def get_schema(self):
        return self.metadata.get_schema()

    def destroy(self):
        del self.metadata
        del self

    def clean_references(self):
        self.metadata.clean_references()

    #Transaction methods overwritten to propagate command to metadata object
    def start(self):
        self.metadata.start()
        super(MeltaBaseObject, self).start()

    def stop(self):
        self.metadata.stop()
        super(MeltaBaseObject, self).stop()

    def commit(self):
        self.metadata.commit()
        super(MeltaBaseObject, self).commit()

    def checkpoint(self):
        self.metadata.checkpoint()
        super(MeltaBaseObject, self).checkpoint()

    def rollback(self):
        self.metadata.rollback()
        super(MeltaBaseObject, self).rollback()

    # Update updated_at when a member of the melta object is modified.
    def __setattr__(self, name, value):
        try:
            super(MeltaBaseObject, self).__getattribute__('metadata') #call object __getattribute__ to not break missing method on AggregationObject
            self.metadata.notify_object_update()
        except AttributeError:
            pass
        return super(MeltaBaseObject, self).__setattr__(name, value)


class AggregationObject(MeltaBaseObject):
    def __init__(self, melta_instance_name=None, primitive_type=INSTANCE_TYPE, *args, **kwargs):
        self._atomic_attributes = []
        self._primitive_type = primitive_type
        super(AggregationObject, self).__init__(melta_instance_name, *args, **kwargs)
        if args:
            self.set_attributes_list(*args)
        if kwargs:
            self.set_attrbutes(**kwargs)


    def get_attributes(self):
        return self._atomic_attributes

    def set_attrbutes(self, **kwargs):
        for name in kwargs:
            self._atomic_attributes.append(AtomicObject(name, kwargs[name]))

    def set_attributes_list(self, *args):
        for melta_object in args:
            if not isinstance(melta_object, MeltaBaseObject):
                raise MeltaException('{0} is not a Melta Object'.format(melta_object))
            self._atomic_attributes.append(melta_object)

    def _find_atomic_attribute_(self, name):
        value = [atomic.value for atomic in self._atomic_attributes if atomic.instance_name == name][0]
        if not value:
            raise NotFoundMeltaObject
        return value

    def syncronize(self, python_object):
        #TODO: create a syncronizer and syncronize objects
        pass

    def get_data_type(self):
        return self._primitive_type

    def get_class(self):
        return self.metadata.original_class

    def destroy(self):
        for atomic in self._atomic_attributes:
            atomic.destroy()
        super(AggregationObject, self).destroy()

    def __getattribute__(self, name):
        """
        Missing method to get values of _atomic_attributes members by just calling their identifier.
        """
        try:
            return super(AggregationObject, self).__getattribute__(name)
        except AttributeError:
            return self._find_atomic_attribute_(name)


class AtomicObject(MeltaBaseObject):
    def __init__(self, melta_instance_name=None, value=None):
        self.value = value
        super(AtomicObject, self).__init__(melta_instance_name)

    def get_data_type(self):
        return type(self.value).__name__

    def get_value(self):
        return self.value


class ReferenceObject(MeltaBaseObject):
    def __init__(self, base_object, melta_instance_name=None):
        self.reference_id = base_object.get_id()
        self.wrapped_object = base_object
        super(ReferenceObject, self).__init__(melta_instance_name)
        base_object.metadata.add_reference(self)

    def get_referenced_object(self):
        return self.wrapped_object

    def get_data_type(self):
        return self.get_referenced_object().get_data_type()

    def destroy(self):
        self.wrapped_object.remove_reference(self)
        super(ReferenceObject, self).destroy()