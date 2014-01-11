import unittest
from melta.dynamic import mutator

class A:
    pass

class AObject(object):
    pass

class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.instanceA = A()
        self.instanceAObj = AObject()

    def testInsertMethod(self):
        code = '''def myFunction(self,value):
                    return value+'22'
             '''
        mutator.Mutator.createFunction(self.instanceA.__class__,code)
        self.assertEqual('122',self.instanceA.myFunction('1'))

    def testInsertMethodObjectException(self):
        code = '''def myFunction(self,value):
                    return value+'22'
             '''
        def call():
            mutator.ObjectMutator.createFunction(self.instanceAObj.__class__,code)
        self.assertRaises(TypeError,call)

    def testInsertMethodObject(self):
            code = '''def myFunction(self,value):
                    return value+'22'
             '''
            mutator.ObjectMutator.createFunction(self.instanceAObj,code)
            self.assertEqual('4422',self.instanceA.myFunction('44'))

if __name__ == '__main__':
    unittest.main()
