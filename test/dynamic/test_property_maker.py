from unittest import TestCase
import inspect
from melta.dynamic.propertyMaker import PropertyMaker, Mutator


class A:
    pass


class B:
    pass


class C:
    def __init__(self, atribute):
        PropertyMaker().buildProperty(self, 'attribute', atribute)


class testDynamicProperty(TestCase):
    def setUp(self):
        self.a = A()

    def test_build_property(self):
        PropertyMaker().buildProperty(self.a, 'saraza', 2)
        self.assertEqual(self.a.saraza, 2)

    def test_build_properties_string(self):
        PropertyMaker().buildProperty(self.a, 'dato', "ddd")
        self.assertEqual(self.a.dato, "ddd")

    def test_build_properties(self):
        PropertyMaker().buildProperties(self.a, {'dato': "ddd", "saraza": 2})
        self.assertEqual(self.a.dato, "ddd")
        self.assertEqual(self.a.saraza, 2)

    def test_assign_instance(self):
        b = B()
        PropertyMaker().buildProperty(self.a, 'instanceB', b)
        self.assertEqual(b, self.a.instanceB)

    def test_glued_code(self):
        prop = PropertyMaker()
        PropertyMaker().migrateMethods(self.a)
        Mutator().rebind(prop.getPrivateMehtods, self.a)
        for methodProp, methodA in (zip(prop.getPrivateMehtods(), self.a.getPrivateMehtods())):
            self.assertEqual(inspect.getsource(methodProp), inspect.getsource(methodA))

    def test_self_attribute_setter(self):
        value = 34
        c_instance = C(value)
        self.assertEqual(value, c_instance.attribute)

    def test_build_properties_chained(self):
        PropertyMaker().buildProperty(self.a, 'data', 3) \
            .buildProperty(self.a, 'something', 'a')
        self.assertEqual(self.a.data, 3)
        self.assertEqual(self.a.something, 'a')


    def test_boolean_property(self):
        PropertyMaker().buildProperty(self.a, 'somthg', False)
        self.assertEqual(self.a.somthg, False)
        self.assertFalse(self.a.somthg)

    def tets_chained_boolean(self):
        PropertyMaker().buildProperty(self.a, 'somthg', False) \
            .buildProperty(self.a, 'prop', 34)
        self.assertEqual(self.a.prop, 34)
        self.assertEqual(self.a.somthg, False)