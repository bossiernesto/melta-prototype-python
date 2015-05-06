from unittest import TestCase, skip
from test.fixture.class_repositories import *
from melta.core.schema import Schema
from melta.core.basicmodel import AtomicObject, AggregationObject, ReferenceObject


class TestSchema(TestCase):
    def setUp(self):
        self.schema = Schema("TestSchema")
        self.atomic = AtomicObject('student_id', '244')
        self.aggregation = AggregationObject('Person', **{'name': 'Mark', 'age': 23})
        self.reference = ReferenceObject(self.atomic)

    def test_created_schema(self):
        self.assertTrue(isinstance(self.schema, Schema))
        self.assertEqual(self.schema.schema_name, "TestSchema")

    def test_add_basictype_objects(self):
        object_types = [self.atomic, self.aggregation, self.reference]
        for object_type in object_types:
            self.schema.add_object(object_type)
            self.assertIn(object_type, self.schema.root_objects)


class TestSchemaFromPython(TestCase):
    def setUp(self):
        self.schema = Schema("AnotherTestSchema")
        self.person_wit_attributes = person1
        self.integer_value = 42
        self.house = house1

    def get_element_root_list(self, position):
        return list(self.schema.root_objects)[position]

    def test_add_atomic_value(self):
        self.schema.add_object(self.integer_value, 'LifeMeaning')
        melta_object = self.get_element_root_list(0)
        self.assertEqual(self.integer_value, melta_object.value)
        self.assertEqual(self.schema, melta_object.get_schema())

    def test_add_persona_object(self):
        person = Person()
        person.name = "Tim"
        person.age = "30"

        self.schema.add_object(person)
        melta_object = self.get_element_root_list(0)
        self.assertEqual(melta_object.age, person.age)
        self.assertEqual(melta_object.name, person.name)


    def test_add_instance_object(self):
        self.schema.add_object(self.person_wit_attributes)
        my_object = self.get_element_root_list(0)
        self.assertEqual(my_object._edad, 20)