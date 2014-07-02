from .utils.random import generate_object_id


class Schema(object):
    def __init__(self, name=None):
        self.obects_name_dictionary = {}
        self.root_objects = set()
        self.objects = set()
        self.schema_id = generate_object_id()
        self.schema_name = name or self.schema_id

    def add_dictionary(self,object):
        pass

    def add_object(self,object):
        pass

    def __repr__(self):
        return 'sss'