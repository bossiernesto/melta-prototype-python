from melta.core.configuration import MeltaConfiguration
from unittest import TestCase


class TestMeltaConfiguration(TestCase):
    def setUp(self):
        self.conf = MeltaConfiguration()

    def test_default_configuration(self):
        self.assertEqual(self.conf.persist_to, 'melta')
        self.assertFalse(self.conf.remove_on_cascade)
        self.assertTrue(self.conf.enable_transactions)

    def test_added_new_configuration(self):
        configuration = MeltaConfiguration(**{'another_feature': 'another'})
        self.assertEqual('another', configuration.another_feature)

    def test_is_property_defined(self):
        self.assertTrue(self.conf.is_property_set('enable_transactions'))
        self.assertFalse(self.conf.is_property_set('a_property'))

    def test_update_inexistent_property(self):
        self.conf._update_property_by_name('a_conf', 'something')
        self.assertEqual('something', self.conf.a_conf)


    def test_overriden_configuration(self):
        configuration = MeltaConfiguration(**{'persist_to': 'json'})
        self.assertEqual('json', configuration.persist_to)
        self.assertTrue(configuration.enable_transactions)

    def test_new_item_configuration(self):
        def get_prop():
            return self.conf.a_property

        self.assertRaises(AttributeError, get_prop)
        self.conf.add_property('a_property', 42)
        self.assertEqual(self.conf.a_property, 42)

    def test_is_defined_sucess(self):
        self.assertTrue(self.conf.is_property_set('persist_to'))

    def test_is_defined_failure(self):
        self.assertFalse(self.conf.is_property_set('another_property'))

    def test_is_defined_add_after(self):
        another_property = 'another_property'
        self.assertFalse(self.conf.is_property_set(another_property))
        self.conf.add_property(another_property)
        self.assertTrue(self.conf.is_property_set(another_property))

    def test_remove_on_cascade(self):
        self.assertFalse(self.conf.remove_on_cascade)
        self.assertFalse(self.conf.can_remove_on_cascade())
        self.conf.remove_on_cascade = True
        self.assertTrue(self.conf.can_remove_on_cascade())