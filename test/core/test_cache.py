from unittest import TestCase
from melta.core.schema import Schema


class MyClass:
    def __init__(self, number):
        self.number = number


class MeltaCacheTest(TestCase):
    def setUp(self):
        self.an_object = MyClass(23)
        self.another_object = MyClass(24)
        self.schema = Schema('TestCacheSchema')

    def test_cache_removal(self):
        self.schema.add_object(self.an_object)
        python_objs_cache = list(self.schema.cache.to_object_cache.data.values())
        self.assertEqual(self.an_object, python_objs_cache[0])
        self.assertEqual(1, len(self.schema.cache.to_melta_object_cache))

        #delete the object to and see if the cache has cleaned
        del self.an_object

        self.assertEqual(1, len(self.schema.cache.to_object_cache))
        self.assertEqual(0, len(self.schema.cache.to_melta_object_cache))
        #because there is a weak ref the user must purge the schema
        self.schema.commit_state()

        self.assertEqual(0, len(self.schema.cache.to_object_cache))

    def test_change_state(self):
        self.schema.add_object(self.an_object)
        self.an_object.number = 34
        self.schema.commit_state()