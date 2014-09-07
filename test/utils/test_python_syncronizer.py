from unittest import TestCase
from melta.dynamic.propertyMaker import PropertyMaker
import copy
from melta.utils.python_syncronizer import PythonSyncronizer


class PyObjectToSyncronize:
    def __init__(self):
        PropertyMaker().buildProperty(self, "un_atributo", 30) \
            .buildProperty(self, "otro_atributo", "algo")


class PySubclassToSyncronize(PyObjectToSyncronize):
    def __init__(self):
        super().__init__()
        PropertyMaker().buildProperty(self, 'another_attr', 130)


class PySubClassObjectToSyncronize(PyObjectToSyncronize):
    def __init__(self):
        #This class inherits from PyObjectSyncronize but it wasn't called the superclass deliberately
        PropertyMaker().buildProperty(self, "an_attr", 50)


class TestSyncronizer(TestCase):
    def setUp(self):
        self.a_object = PyObjectToSyncronize()
        self.another_object = copy.deepcopy(self.a_object)
        self.syncronizer = PythonSyncronizer()

        self.subclass_object = PyObjectToSyncronize()
        self.invalid_subclass = PySubClassObjectToSyncronize()

    def tearDown(self):
        del (self.a_object)
        del (self.another_object)

    def get_instance_from_random_class(self):
        class RandomClass():
            pass

        return RandomClass()

    def test_succesful_syncronization(self):
        self.a_object.un_atributo = 'something'
        self.assertEqual(self.another_object.un_atributo, 30)
        self.syncronizer.syncronize(self.a_object, self.another_object)
        self.assertEqual(self.another_object.un_atributo, "something")

    def test_multiple_changes_syncronization(self):
        self.a_object.un_atributo = 340
        self.a_object.otro_atributo = 334
        self.syncronizer.syncronize(self.a_object, self.another_object)
        self.assertEqual(self.another_object.un_atributo, 340)
        self.assertEqual(self.another_object.otro_atributo, 334)

    def test_no_syncronization(self):
        self.assertEqual(self.another_object.un_atributo, 30)
        self.syncronizer.syncronize(self.a_object, self.another_object)
        self.assertEqual(self.another_object.un_atributo, 30)

    def test_invalid_classes_syncronization(self):
        self.another_object.un_atributo = "something"
        another_instance = self.get_instance_from_random_class()
        with self.assertRaises(Exception):
            self.syncronizer.syncronize(self.another_object, another_instance)

    def test_subclass_with_different_attributes(self):
        self.invalid_subclass.an_attr = 453
        with self.assertRaises(Exception):
            self.syncronizer.syncronize(self.invalid_subclass, self.a_object)

    def test_subclass_with_same_attributes(self):
        self.a_object.otro_atributo = 50
        self.assertEqual(self.subclass_object.otro_atributo, "algo")
        self.syncronizer.syncronize(self.a_object, self.subclass_object)
        self.assertEqual(self.subclass_object.otro_atributo, 50)



