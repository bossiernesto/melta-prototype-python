from .random import generate_object_id
from melta.exceptions.exceptions import MeltaException
from .object_converter import MeltaObjectConverter
from .cache import MeltaCache
from melta.utils.utils import is_python_instance
from .metadata import MetadataSchema
from melta.transactions.transactional import Transaction

class Schema(object, Transaction):
    def __init__(self, name=None):
        self.schema_id = generate_object_id()
        self.schema_name = name or self.schema_id

        #cache and metadata facilities
        self.synchronization_strategy = None #TODO: add some synchronization strategies
        self.cache = MeltaCache()
        self.metadata = MetadataSchema(self)

        #set of root_objects in the current schema
        self.root_objects = set()
        #set ob all the objects on the current schema or database
        self.objects = {}


    def to_object(self, query):
        pass

    def merge_with(self, other_schema):
        """
        merge current schema with other existing schema. Should add new objects to
        """
        pass

    def add_melta_object(self, melta_object):
        from melta.core.basicmodel import MeltaBaseObject

        if not isinstance(melta_object, MeltaBaseObject):
            raise MeltaException(
                "Cannot add a non melta object to the model, use add_object for adding a python object")
        self.root_objects.add(melta_object)
        self.objects[melta_object.get_id()] = melta_object

    def to_melta_object(self, object, alternate_name=None, transactions=False):
        return MeltaObjectConverter().to_melta_object(object, alternate_name=None, transactions=False)

    def add_object(self, object, transactions=False, alternate_name=None):
        cache = is_python_instance(object)
        self.add_object_to_schema(object, cache, transactions)

    def add_object_to_schema(self, object, cache=True, transactions=False, alternate_name=None):
        from melta.core.basicmodel import MeltaBaseObject

        try:
            original_object = object
            if isinstance(object, MeltaBaseObject):
                melta_object = object
            else:
                melta_object = self.to_melta_object(object, alternate_name, transactions)
                self.cache.add_object(melta_object, original_object)
            self.add_melta_object(melta_object)
        except MeltaException:
            #TODO: log event
            pass


    def __repr__(self):
        return '<MeltaSchema {0} id: {1}> with root_objects:{2} and objects: {3}'.format(self.schema_name,
                                                                                         self.schema_id,
                                                                                         repr(self.root_objects),
                                                                                         repr(self.objects))