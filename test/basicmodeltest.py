from unittest import TestCase
from melta.basicmodel import AtomicObject


class BasicModelTest(TestCase):
    def setup(self):
        pass

    def test_atomic_object(self):
        new_atomic_object = AtomicObject(**{'name': 'Mark', 'age': 23})
        self.assertEqual(new_atomic_object.name,'Mark')
        self.assertEqual(new_atomic_object.age,23)