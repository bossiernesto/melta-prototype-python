from unittest import TestCase
from melta.core.basicmodel import AggregationObject, AtomicObject


class AtomicModelTest(TestCase):
    def test_create_valid_atomic_object(self):
        atomic = AtomicObject(None, 2)
        self.assertEqual(atomic.value, 2)
        self.assertTrue(atomic.instance_name.startswith('AtomicObject'))

    def test_create_null_value_object(self):
        atomic = AtomicObject('PersonID')
        self.assertEqual(atomic.value, None)
        self.assertEqual(atomic.instance_name,'PersonID')


class AggregationModelTest(TestCase):
    def setup(self):
        pass

    def test_aggregated_object(self):
        new_atomic_object = AggregationObject(**{'name': 'Mark', 'age': 23})
        self.assertEqual(new_atomic_object.name, 'Mark')
        self.assertEqual(new_atomic_object.age, 23)