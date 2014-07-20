from melta.dynamic.propertyMaker import PropertyMaker
import datetime
from melta.core.melta_types import INSTANCE_TYPE
from melta.transactions.transactional import Transaction


class Metadata(Transaction, object):
    pass


class MetadataSchema(Metadata):
    def __init__(self, schema, created_at=datetime.datetime.now()):
        PropertyMaker().buildProperty(self, 'schema', schema)
        #objects_name_space is a dictionary with Melta object name key and a set of melta objects with that name identifier.
        self.objects_name_space = {}
        PropertyMaker().buildProperty(self, 'created_at', created_at) \
            .buildProperty(self, 'object_count', 0)

    def remove_object_from_space(self, melta_object):
        object_set = self.objects_name_space[melta_object.instance_name]
        self.objects_name_space[melta_object.instance_name] = object_set.difference([melta_object])

    def update_object_space(self, melta_object):
        """
        Update the objects_name_space with a new object
        """
        try:
            object_set = self.objects_name_space[melta_object.instance_name]
            object_set.add(melta_object)
        except KeyError:
            new_set = set()
            new_set.add(melta_object)
            self.objects_name_space[melta_object.instance_name] = new_set


CLEAN_MELTAOBJECT_STATUS = 'clean'
DIRTY_MELTAOBJECT_STATUS = 'dirty'
INVALID_MELTAOBJECT_STATUS = 'invalid'

OBJECT_STATUS = [CLEAN_MELTAOBJECT_STATUS, DIRTY_MELTAOBJECT_STATUS, INVALID_MELTAOBJECT_STATUS]


class MetadataObject(Metadata):
    def __init__(self, object):
        original_class = object.instance_name if object.get_data_type() == INSTANCE_TYPE else None
        PropertyMaker().buildProperty(self, 'created_at', datetime.datetime.now()) \
            .buildProperty(self, 'modified_at', datetime.datetime.now()) \
            .buildProperty(self, 'object', object) \
            .buildProperty(self, 'schema') \
            .buildProperty(self, 'object_status', CLEAN_MELTAOBJECT_STATUS) \
            .buildProperty(self, 'original_class', original_class) \
            .buildProperty(self, 'object_references', set())

    def notify_object_update(self):
        self.modified_at = datetime.datetime.now()

    def get_schema(self):
        return self.schema

    def add_reference(self, reference):
        self.object_references.add(reference)

    def remove_reference(self, reference):
        self.object_references = self.object_references.difference([reference])

    def clean_references(self):
        self.object_references = set()