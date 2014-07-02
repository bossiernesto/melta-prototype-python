from unittest import TestCase
from test.fixture.class_repositories import *
from melta.core.schema import Schema

class TestSchema(TestCase):
    def setUp(self):
        self.schema = Schema("TestSchema")

    def test_created_schema(self):
        self.assertTrue(isinstance(self.schema, Schema))
        self.assertEqual(self.schema.schema_name, "TestSchema")

    #TODO: add Python objects and dictionaries and test them

