from unittest import TestCase
from test.fixture.class_repositories import *
from melta.core.schema import Schema
from melta.core.basicmodel import AtomicObject, AggregationObject


class TestSchema(TestCase):
    def setUp(self):
        self.schema = Schema("TestSchema")
        self.atomic = AtomicObject('student_id', '244')

    def test_created_schema(self):
        self.assertTrue(isinstance(self.schema, Schema))
        self.assertEqual(self.schema.schema_name, "TestSchema")

    #TODO: add Python objects and dictionaries and test them
    def test_add_object(self):
        self.schema.add_object(self.atomic)
        self.assertIn(self.atomic, self.schema.root_objects)


