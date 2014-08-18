from unittest import TestCase
from melta.dynamic.propertyMaker import PropertyMaker
import copy

class PyOBjectToSyncronize:

    def __init__(self):
        PropertyMaker().buildProperty(self,"un_atributo",30)\
                       .buildProperty(self,"otro_atributo","algo")


class TestSyncronizer(TestCase):

    def setUp(self):

        a_object = PyOBjectToSyncronize()
        another_object = copy.deepcopy(a_object)

