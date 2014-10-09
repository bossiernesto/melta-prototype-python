__author__ = 'ernesto'


def is_ancestor_present(instance, ancestor_class):
    return ancestor_class in get_ancestors(instance.__class__)


def is_subclass(a_class, another_class):
    return issubclass(a_class, another_class) and a_class != another_class


def get_ancestors(clazz):
    return (clazz.__bases__ + (clazz,))


class PythonSyncronizer(object):
    def __init__(self, ignore_private_attrs=False, ignore_attrs_name=[]):
        self.ignore_private_attrs = ignore_private_attrs
        self.ignore_attrs_name = ignore_attrs_name
        self.private_startwith = "_"

    def syncronize(self, from_object, to_object, side_effects=False):
        clazz_hierarchy = from_object.__class__

        if not self._to_class_same_hierarchy(to_object, clazz_hierarchy):
            raise PythonSyncronizerException('instance {0} is not included in the hierarchy of {1}, '
                                             'with class hierarchy {2}'.format(to_object, from_object,
                                                                               get_ancestors(clazz_hierarchy)))

        self._syncronize_objects(from_object, to_object, side_effects)

    def ignore_private_attributes(self, attr_list):
        return [value for value in attr_list if not value.startswith(self.private_startwith)] \
            if self.ignore_private_attrs else attr_list

    def ignore_custom_attributes(self, attr_list):
        return [value for value in attr_list if not value in self.ignore_attrs_name] \
            if len(self.ignore_attrs_name) > 0 else attr_list

    def _get_attributes(self, instance):
        attributes_names = [name for name in iter(vars(instance))]
        attributes_names = self.ignore_private_attributes(attributes_names)
        attributes_names = self.ignore_custom_attributes(attributes_names)
        return attributes_names

    def _syncronize_objects(self, from_object, to_object, side_effects=False):
        attributes_from = self._get_attributes(from_object)

        for attribute in attributes_from:
            value_to_sync = getattr(from_object, attribute)
            setattr(to_object, attribute, value_to_sync)


    def _to_class_same_hierarchy(self, to_object, clazz):
        return is_ancestor_present(to_object, clazz) \
            and (not is_subclass(clazz, to_object.__class__))


class PythonSyncronizerException(Exception):
    pass
