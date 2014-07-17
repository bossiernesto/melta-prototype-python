from melta.dynamic.propertyMaker import PropertyMaker


class MeltaConfiguration(object):
    def __init__(self, *args, **kwargs):
        PropertyMaker().buildProperty(self, 'persist_to', 'melta') \
            .buildProperty(self, 'remove_on_cascade', False) \
            .buildProperty(self, 'enable_transactions', True) \
            .buildProperty(self, 'syncronization_strategy', None)
        for k, v in kwargs.items():
            self._update_property_by_name(k, v)


    def _update_property_by_name(self, property_name, value):
        if not self.is_property_set(property_name):
            return self.add_property(property_name, value)
        setattr(self, '_'+property_name, value)

    def is_property_set(self, property):
        try:
            getattr(self, property)
            return True
        except AttributeError:
            return False

    def add_property(self, property_name, property_value=None):
        PropertyMaker().buildProperty(self, property_name, property_value)

    def generic_check_boolean_value(self,property_name):
        return getattr(self,property_name)

    can_remove_on_cascade = lambda self: self.generic_check_boolean_value('remove_on_cascade')