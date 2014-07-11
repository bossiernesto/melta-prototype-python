from unittest import TestCase
from melta.core.object_converter import StringConverter, InstanceConverter, IntegerConverter, ListConverter, DictionaryConverter
from melta.core.basicmodel import AtomicObject, AggregationObject


class TestingPerson(object):
    def __init__(self):
        self.age = None
        self.name = None


class MeltaConverterTest(TestCase):
    def setUp(self):
        self.string_converter = StringConverter()
        self.integer_converter = IntegerConverter()
        self.instance_converter = InstanceConverter()
        self.list_converter = ListConverter()
        self.dictionary_converter = DictionaryConverter()

    def test_convert_integer(self):
        integer = 34
        melta_atomic = self.integer_converter.to_melta_object(integer)
        self.assertIsInstance(melta_atomic, AtomicObject)
        self.assertEqual(melta_atomic.value, integer)
        self.assertEqual(integer, self.integer_converter.to_object(melta_atomic))

    def test_convert_string(self):
        my_string = "Hello world"
        melta_atomic = self.string_converter.to_melta_object(my_string)
        self.assertIsInstance(melta_atomic, AtomicObject)
        self.assertEqual(melta_atomic.value, my_string)
        self.assertEqual(my_string, self.string_converter.to_object(melta_atomic))

    def test_instance_converter(self):
        testing_person = TestingPerson()
        testing_person.age = 23
        testing_person.name = 'Jane'

        aggregation_object = self.instance_converter.to_melta_object(testing_person)
        self.assertIsInstance(aggregation_object, AggregationObject)
        self.assertEqual(23, aggregation_object.age)
        self.assertEqual('Jane', aggregation_object.name)
        new_testing_person = self.instance_converter.to_object(aggregation_object)

        self.assertEqual(testing_person.__class__, new_testing_person.__class__)
        self.assertEqual(testing_person.age, new_testing_person.age)
        self.assertEqual(testing_person.name, new_testing_person.name)

        self.assertNotEqual(testing_person, new_testing_person)

    def test_simple_list_converter(self):
        simple_list = ["Hi", 23, 1]
        aggregation_object = self.list_converter.to_melta_object(simple_list)
        self.assertIsInstance(aggregation_object, AggregationObject)
        self.assertEqual("Hi", aggregation_object.get_attributes()[0].value)
        self.assertEqual(23, aggregation_object.get_attributes()[1].value)
        self.assertEqual(1, aggregation_object.get_attributes()[2].value)
        self.assertEqual(simple_list, self.list_converter.to_object(aggregation_object))