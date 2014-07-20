from unittest import TestCase
from melta.core.basicmodel import AggregationObject, AtomicObject, ReferenceObject


class AtomicModelTest(TestCase):
    def test_create_valid_atomic_object(self):
        atomic = AtomicObject(None, 2)
        self.assertEqual(atomic.value, 2)
        self.assertTrue(atomic.instance_name.startswith('AtomicObject'))

    def test_create_null_value_object(self):
        atomic = AtomicObject('PersonID')
        self.assertEqual(atomic.value, None)
        self.assertEqual(atomic.instance_name, 'PersonID')

    def test_update_value_check_updated_at(self):
        atomic = AtomicObject('PersonaID', 34)
        created_at = atomic.get_metadata().created_at
        modified_at = atomic.get_metadata().modified_at
        atomic.value = 32
        self.assertNotEqual(34, atomic.get_value())
        self.assertEqual(32, atomic.get_value())
        self.assertGreater(atomic.get_metadata().modified_at, modified_at)
        self.assertEqual(created_at, atomic.get_metadata().created_at)


class AggregationModelTest(TestCase):
    def setUp(self):
        self.new_atomic_object = AggregationObject(**{'name': 'Mark', 'age': 23})

    def test_aggregated_object(self):
        self.assertEqual(self.new_atomic_object.name, 'Mark')
        self.assertEqual(self.new_atomic_object.age, 23)


class PointerModelTest(TestCase):
    def setUp(self):
        self.atomic = AtomicObject('Estudiante', 234)
        self.aggregated = AggregationObject(**{'name': 'John', 'age': 54})

    def test_pointer_atomic_object(self):
        reference = ReferenceObject(self.atomic, 'to_student24')
        self.assertEqual(reference.get_referenced_object(), self.atomic)

    def test_pointer_aggregated_object(self):
        reference = ReferenceObject(self.aggregated, 'to_teacher')
        self.assertEqual(reference.get_referenced_object(), self.aggregated)