from unittest import TestCase
from test.fixture.class_repositories import person1, house2
from melta.core.object_converter import MeltaObjectConverter
from melta.core.melta_syncronizer import MeltaSyncronizer
import copy


class TestSyncronizer(TestCase):
    def setUp(self):
        #self.syncronizer = Syncronizer()

        #    house2 object
        #    house2 => "building_age", 34
        #    house2 => "material", "brick"
        #    house2 => "sq2mts", 453

        self.house2 = house2
        self.converter = MeltaObjectConverter()
        self.melta_house2 = self.converter.to_melta_object(self.house2)
        self.melta_house2_deepcopy = copy.deepcopy(self.melta_house2) #keep a deepcopy of the object to compare

    def test_no_syncronization(self):
        #syncronzation should be melta_object => python_object, with side effect 1 as default value,
        # if default value is 0 a new melta object is created and returned, but identity is lost by enabling this last value.
        self.syncronizer.syncronize(self.melta_house2, self.house2, side_effect=True)
        self.assertEqual(self.melta_house2, self.melta_house2_deepcopy)

    def test_syncronization(self):
        self.house2.building_age = 45
        self.syncronizer.syncronize(self.melta_house2, self.house2)
        self.assertNotEqual(self.melta_house2, self.melta_house2_deepcopy)
        self.assertEqual(45, self.melta_house2.building_age)
        self.assertEqual(self.house2.building_age, self.melta_house2.building_age)
        self.assertLess(self.melta_house2_deepcopy.building_age, self.melta_house2.building_age)

    def test_double_syncronization(self):
        self.house2.building_age = 20
        self.syncronizer.syncronize(self.melta_house2, self.house2)
        self.assertEqual(20, self.melta_house2.building_age)

        self.house2.material = "concrete"
        self.assertNotEqual(self.house2.material, self.melta_house2.material)
        self.assertEqual('brick', self.melta_house2.material)
        self.syncronizer.syncronize(self.melta_house2, self.house2)

        self.assertEqual(self.house2.material, self.melta_house2.material)
        self.assertEqual('concrete', self.melta_house2.material)

    def test_nosideeffect_syncronization(self):
        from melta.core.basicmodel import AggregationObject

        self.house2.building_age = 130
        new_object = self.syncronizer.syncronize(self.melta_house2, self.house2, side_effect=False)
        self.assertNotEqual(self.melta_house2, new_object)
        self.assertTrue(isinstance(new_object, AggregationObject))
        self.assertEqual(self.house2.__class__, new_object.get_class())