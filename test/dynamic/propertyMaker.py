from unittest import TestCase
import inspect
from melta.dynamic.propertyMaker import PropertyMaker, Mutator


class A:
    pass


class testDynamicProperty(TestCase):
    def setUp(self):
        self.a = A()

    def testBuildProperty(self):
        PropertyMaker().buildProperty(self.a, 'saraza', 2)
        self.assertEqual(self.a.saraza, 2)

    def testBuildPropertiesString(self):
        PropertyMaker().buildProperty(self.a, 'dato', "ddd")
        self.assertEqual(self.a.dato, "ddd")

    def testBuildProperties(self):
        PropertyMaker().buildProperties(self.a, {'dato': "ddd", "saraza": 2})
        self.assertEqual(self.a.dato, "ddd")
        self.assertEqual(self.a.saraza, 2)

    def testAssignInstance(self):
        class B:
            pass

        b = B()
        PropertyMaker().buildProperty(self.a, 'instanceB', b)
        self.assertEqual(b, self.a.instanceB)

    def testCode(self):
        prop = PropertyMaker()
        PropertyMaker().migrateMethods(self.a)
        Mutator().rebind(prop.getPrivateMehtods, self.a)
        for methodProp, methodA in (zip(prop.getPrivateMehtods(), self.a.getPrivateMehtods())):
            self.assertEqual(inspect.getsource(methodProp), inspect.getsource(methodA))