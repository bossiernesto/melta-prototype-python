from .mutator import Mutator
from .checker import isObjOfType
import inspect


def _makeProperty(self, propertyName, value):
    fget = lambda self: self._getProperty(propertyName)
    fset = lambda self, value: self._setProperty(propertyName, value)
    setattr(self.__class__, propertyName, property(fget, fset))
    setattr(self, self._getAttrName(propertyName), value)


class PropertyMaker:
    def _getAttrName(self, propertyName):
        return '_' + propertyName

    def _setProperty(self, propertyName, value):
        setattr(self, self._getAttrName(propertyName), value)

    def _getProperty(self, propertyName):
        return getattr(self, self._getAttrName(propertyName))

    def _makeProperty(self, propertyName, value):
        fget = lambda self: self._getProperty(propertyName)
        fset = lambda self, value: self._setProperty(propertyName, value)
        setattr(self.__class__, propertyName, property(fget, fset))
        setattr(self, self._getAttrName(propertyName), value)

    def getPrivateMehtods(self):
        return [i for m, i in inspect.getmembers(self, predicate=inspect.ismethod) if '_' in m]

    def migrateMethods(self, target):

        methods = self.getPrivateMehtods()
        for method in methods:
            Mutator().rebind(method, target)

    def buildProperties(self, target, propdict):
        if isObjOfType(propdict, dict):
            for propertName, value in propdict.items():
                self.buildProperty(target, propertName, value)

    def buildProperty(self, target, propertyName, value=None):

        self.migrateMethods(target)
        target._makeProperty(propertyName, value)
        return self