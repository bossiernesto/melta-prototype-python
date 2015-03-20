from unittest import TestCase
from melta.core.object_converter import StringConverter, InstanceConverter, IntegerConverter, ListConverter, \
    DictionaryConverter, TupleConverter, FloatConverter
from melta.core.basicmodel import AtomicObject, AggregationObject


class TestingPerson(object):
    def __init__(self):
        self.age = None
        self.name = None


class MeltaconversionTest(TestCase):
    def setUp(self):
        self.string_converter = StringConverter()
        self.integer_converter = IntegerConverter()
        self.instance_converter = InstanceConverter()
        self.list_converter = ListConverter()
        self.dictionary_converter = DictionaryConverter()
        self.tuple_converter = TupleConverter()
        self.float_converter = FloatConverter()

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

    def test_instance_conversion(self):
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

    def test_simple_list_conversion(self):
        simple_list = ["Hi", 23, 1]
        aggregation_object = self.list_converter.to_melta_object(simple_list)
        self.assertIsInstance(aggregation_object, AggregationObject)
        self.assertEqual("Hi", aggregation_object.get_attributes()[0].value)
        self.assertEqual(23, aggregation_object.get_attributes()[1].value)
        self.assertEqual(1, aggregation_object.get_attributes()[2].value)
        self.assertEqual(simple_list, self.list_converter.to_object(aggregation_object))

    def test_simple_tuple_conversion(self):
        simple_tuple = ["Converter", 345, 5, 2]
        aggregation_object = self.tuple_converter.to_melta_object(simple_tuple)
        self.assertIsInstance(aggregation_object, AggregationObject)
        self.assertEqual("Converter", aggregation_object.get_attributes()[0].value)
        self.assertEqual(345, aggregation_object.get_attributes()[1].value)
        self.assertEqual(simple_tuple, self.tuple_converter.to_object(aggregation_object))

    def test_simple_float_conversion(self):
        simple_float = 34.34
        float_object = self.float_converter.to_melta_object(simple_float)
        self.assertIsInstance(float_object, AtomicObject)
        self.assertEqual(34.34, float_object.get_value())

    def test_chained_list_conversion(self):
        chained_list = [244, 'ans', [298, 61]]
        aggregation_object = self.list_converter.to_melta_object(chained_list)
        self.assertIsInstance(aggregation_object, AggregationObject)
        self.assertIsInstance(aggregation_object.get_attributes()[2], AggregationObject)
        self.assertIsInstance(aggregation_object.get_attributes()[1], AtomicObject)
        self.assertEqual(chained_list, self.list_converter.to_object(aggregation_object))
        self.assertEqual([298, 61], self.list_converter.to_object(aggregation_object.get_attributes()[2]))

    def test_instance_with_list(self):
        instance_with_list = TestingPerson()
        instance_with_list.age = 34
        instance_with_list.name = {'Name': 'John', 'SSN': 1234}

        melta_object = self.instance_converter.to_melta_object(instance_with_list)
        self.assertIsInstance(melta_object, AggregationObject)
        self.assertIsInstance(melta_object.get_attributes()[1], AggregationObject)
        self.assertIsInstance(melta_object.get_attributes()[0], AtomicObject)
        new_instance = self.instance_converter.to_object(melta_object)

        # identity is lost over here
        self.assertNotEqual(new_instance, instance_with_list)
        self.assertEqual(new_instance.age, instance_with_list.age)
        self.assertEqual(new_instance.name, instance_with_list.name)
