from melta.dynamic.propertyMaker import PropertyMaker
import datetime


class Metadata(object):
    pass


class MetadataSchema(Metadata):
    def __init__(self, schema, created_at=datetime.datetime.now()):
        PropertyMaker().buildProperty(self, 'schema', schema)
        #objects_name_space is a dictionary with Melta object name key and a set of objects with this
        self.objects_name_space = {}
        PropertyMaker().buildProperty(self, 'created_at', created_at)
        PropertyMaker().buildProperty(self, 'object_count', 0)

    def update_object_space(self,object):
        """
        Update the objects_name_space with a new object
        """
        pass

class MetadataObject(Metadata):
    def __init__(self, object):
        PropertyMaker().buildProperty(self, 'object', object)
        PropertyMaker().buildProperty(self, 'schema')
        PropertyMaker().buildProperty(self, 'type')

    def get_schema(self):
        return self.schema

