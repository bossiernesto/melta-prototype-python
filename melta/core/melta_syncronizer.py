__author__ = 'ernesto'

from melta.utils.python_syncronizer import PythonSyncronizer, PythonSyncronizerException, get_ancestors
from melta.core.basicmodel import MeltaBaseObject


def is_class_ancestor_present(klass, ancestor_class):
    return ancestor_class in get_ancestors(klass)


class MeltaSyncronizer(PythonSyncronizer):
    def __init__(self, ignore_private_attrs=False, ignore_attrs_name=[]):
        super().__init__(ignore_private_attrs, ignore_attrs_name)
        self.strategy_converter = None


    def syncronize(self, from_object, to_object, side_effects=False):
        if self.same_class(from_object, to_object):
            return super().syncronize(from_object, to_object)

        if self.is_melta_object(from_object):
            return self.melta_to_object_sync(from_object, to_object, side_effects)
        elif self.is_melta_object(to_object):
            return self.object_to_melta_sync(from_object, to_object, side_effects)
        else:
            return super().syncronize(from_object, to_object)

    def is_melta_object(self, an_object):
        super()._to_class_same_hierarchy(an_object, MeltaBaseObject)

    def same_class(self, an_object, another_object):
        return an_object.__class__ == another_object.__class__


    def melta_to_object_sync(self, from_object, to_object, side_effects):
        pass

    def object_to_melta_sync(self, from_object, to_object, side_effects):
        pass

    def _syncronize_objects(self, from_object, to_object, side_effects=False):
        pass


class MeltaSyncronizerException(PythonSyncronizerException):
    pass