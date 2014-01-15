from unittest import TestCase
from melta.basicmodel import AggregationObject, AtomicObject


class AtomicModelTest(TestCase):
    def test_create_valid_atomic_object(self):
        atomic = AtomicObject(None, 2)
        self.assertEqual(atomic.value, 2)
        self.assertTrue(atomic.instance_name.startswith('AtomicObject'))

    def test_create_named_atomic_object(self):
        atomic = AtomicObject('PersonID', 23)
        self.assertEqual(atomic.value, 23)
        self.assertEqual(atomic.instance_name, 'PersonID')

    def test_create_invalid_atomic_object(self):
        from melta.basicmodel import AtomicObjectInvalidArgumentsException

        self.assertRaises(AtomicObjectInvalidArgumentsException, AtomicObject, 'PersonID', 24, 2)

    def test_create_null_value_object(self):
        atomic = AtomicObject('PersonID')
        self.assertEqual(atomic.value, None)


class AggregationModelTest(TestCase):
    def setup(self):
        pass

    def test_aggregated_object(self):
        new_atomic_object = AggregationObject(**{'name': 'Mark', 'age': 23})
        self.assertEqual(new_atomic_object.name, 'Mark')
        self.assertEqual(new_atomic_object.age, 23)