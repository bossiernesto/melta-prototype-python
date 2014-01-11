import types
from inspect import isclass

class Mutator:

    @staticmethod
    def unbind(f):
        self = getattr(f, '__self__', None)
        if self is not None and not isinstance(self, types.ModuleType) and not isinstance(self, type):
            if hasattr(f, '__func__'):
                return f.__func__
            return getattr(type(f.__self__), f.__name__)
        raise TypeError('not a bound method')

    @staticmethod
    def bind(f, obj):
        obj.__dict__[f.__name__] = types.MethodType(f,obj,obj.__class__)

    @staticmethod
    def rebind(f, obj):
        Mutator.bind(Mutator.unbind(f),obj)

    @staticmethod
    def createFunction(klass, code):
        dict = {}
        methodName = Mutator.getSignatureString(code)
        exec(code.strip(),globals(), dict)
        Mutator.insertFunction(klass, dict, methodName)

    @staticmethod
    def insertFunction(klass, dictMethod, methodName):
        setattr(klass,methodName,dictMethod[methodName])
        return klass.__dict__[methodName]

    @staticmethod
    def getSignatureString(methodString):
        return methodString[methodString.find("def") + 3:methodString.find("(")].strip()


class ObjectMutator(Mutator):

    @staticmethod
    def createFunction(instance, code):
        if isclass(instance):
            raise TypeError("Should pass an instance and not the class")
        Mutator.createFunction(instance,code)