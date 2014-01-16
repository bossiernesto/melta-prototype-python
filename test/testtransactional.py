from unittest import TestCase
from melta.transactions.transactional import Transaction


class TransactionTestClass(Transaction):
    def __init__(self):
        self.plant_type = 'Pointisera'
        self.plant_age = 3
        self.plant_pot = 'plastic'
        self.combination = 'one\ntwo\nthree'


class TransactionalTestCase(TestCase):
    def setUp(self):
        self.test_plant = TransactionTestClass()
        self.test_plant.start()

    def test_succesful_transaction(self):
        self.test_plant.age = 4
        self.test_plant.commit()
        self.assertEqual(self.test_plant.age, 4)


    def test_unsuccesful_transaction(self):
        clay = 'Clay'
        self.test_plant.plant_pot = clay
        self.test_plant.rollback()

        self.assertNotEqual(self.test_plant.plant_pot, clay)
        self.assertEqual(self.test_plant.plant_pot,'plastic')

    def test_multiline_string_transaction(self):
        another_combination = 'one\nnine\nfive'
        new_combination = 'one\nnine\nthree'

        self.test_plant.combination = new_combination
        self.test_plant.commit()
        self.assertEqual(self.test_plant.combination, new_combination)
        self.test_plant.start()
        self.test_plant.combination = another_combination
        self.test_plant.rollback()
        self.assertEqual(self.test_plant.combination, new_combination)