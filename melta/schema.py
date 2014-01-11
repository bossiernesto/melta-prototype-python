from .random import generate_object_id


class Schema(object):

    def __init__(self, name=None):
        self.root_objects = set()
        self.objects = set()
        self.schema_id = generate_object_id()
        self.schema_name = self.schema_id or name

    def __repr__(self):
        return 'sss'