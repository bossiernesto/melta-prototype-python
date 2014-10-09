from unittest import TestCase
from melta.utils.plugin import PluginMount

#testting class
class A:
    def get_plugins(self):
        return self.state_provider.__class__.get_plugins()

#State Provider that implements the Plugin Prototype
class StateProvider(metaclass=PluginMount):
    def perform(self, instance):
        raise NotImplementedError


class UpdateState(StateProvider):
    def perform(self, instance):
        instance.state = 12


class Update(StateProvider):
    def perform(self, instance):
        instance.update_another_state = 23


class PluginTestCase(TestCase):
    def setUp(self):
        self.instance = A()
        self.instance.state_provider = StateProvider()

    def test_plugin(self):
        for action in self.instance.get_plugins():
            action.perform(self.instance)
        self.assertEqual(self.instance.state, 12)
        self.assertEqual(self.instance.update_another_state, 23)




