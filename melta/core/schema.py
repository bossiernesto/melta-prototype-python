from .random import generate_object_id
from melta.exceptions.exceptions import MeltaException
from .object_converter import MeltaObjectConverter
from .cache import MeltaCache
from melta.utils.utils import is_python_instance
from .metadata import MetadataSchema
from melta.transactions.transactional import Transaction
import gc
from melta.core.configuration import MeltaConfiguration


class Schema(Transaction, object):
    def __init__(self, name=None, configuration=None):
        self.schema_id = generate_object_id()
        self.schema_name = name or self.schema_id
        self.configuration = configuration or MeltaConfiguration()

        #cache and metadata facilities
        self.syncronizer = None #TODO: add some synchronization strategies based on it's configuration
        self.cache = MeltaCache(self)
        self.metadata = MetadataSchema(self)

        #set of root_objects in the current schema
        self.root_objects = set()
        #set ob all the objects on the current schema or database
        self.objects = {}

    def get_configuration(self):
        return self.configuration

    def convert_to_object(self, query):
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
        self.metadata.update_object_space(melta_object)
        melta_object.added_to_schema(self)

    def commit_state(self):
        self.cache.update_cache()

    def to_melta_object(self, python_object, alternate_name=None):
        return MeltaObjectConverter().to_melta_object(python_object, alternate_name=None)

    def add_object(self, python_object, alternate_name=None):
        cache = is_python_instance(python_object)
        self.add_object_to_schema(python_object, cache, alternate_name)

    def _clean_references_on_current_schema(self, melta_object):
        references = melta_object.metadata.object_references
        melta_object.clean_references()
        for reference in references:
            self.remove_object(reference)


    def remove_object(self, melta_object):
        from melta.core.basicmodel import MeltaBaseObject

        if not isinstance(melta_object, MeltaBaseObject):
            raise MeltaException('Object {0} is not of {1}'.format(melta_object, MeltaBaseObject.__name__))
        current_object = self.objects.pop(melta_object.get_id())
        self._clean_references_on_current_schema(melta_object)
        self.root_objects = self.root_objects.difference([melta_object])
        self.metadata.remove_object_from_space(current_object)
        current_object.destroy()
        del current_object
        gc.collect()

    def add_object_to_schema(self, python_object, cache=True, alternate_name=None):
        from melta.core.basicmodel import MeltaBaseObject

        try:
            original_object = python_object
            if isinstance(python_object, MeltaBaseObject):
                melta_object = python_object
            else:
                melta_object = self.to_melta_object(python_object, alternate_name)
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