from unittest import TestCase
from melta.core.basicmodel import AtomicObject, AggregationObject, ReferenceObject
import datetime

class TestMeltaObjectsTransaction(TestCase):
    def setUp(self):
        self.atomic = AtomicObject('meaning_of_life', 42)
        self.aggregation = AggregationObject('Car', **{'model': 1934, 'brand': 'Ford'})
        self.referal = AtomicObject('Text', 'Hello World!')
        self.reference = ReferenceObject(self.referal)

    def test_atomic_transaction(self):
        self.atomic.start()
        self.atomic.stop()
        self.assertEqual(self.atomic.value, 42)

    def test_atomic_with_change(self):
        self.atomic.start()
        self.atomic.value = 34
        self.atomic.commit()
        self.assertEqual(self.atomic.value, 34)

    def test_atomic_rollback(self):
        self.atomic.start()
        self.atomic.value = 53
        self.assertEqual(self.atomic.value, 53)
        self.atomic.rollback()
        self.assertEqual(self.atomic.value, 42)

    def test_atomic_with_checkpoint(self):
        self.atomic.start()
        self.atomic.value = 34
        self.atomic.checkpoint()
        self.assertEqual(self.atomic.value, 34)
        self.atomic.value = 55
        self.atomic.rollback()
        self.assertEqual(self.atomic.value, 34)

    def test_atomic_propagation_to_meta(self):
        self.atomic.start()
        now = datetime.datetime.now()
        old_modified_at = self.atomic.metadata.modified_at
        self.atomic.metadata.modified_at = now
        self.atomic.commit()
        self.assertEqual(self.atomic.metadata.modified_at, now)
        self.assertGreater(self.atomic.metadata.modified_at, old_modified_at)


    def test_atomic_propagation_rollback(self):
        self.atomic.start()
        now = datetime.datetime.now()
        old_modified_at = self.atomic.metadata.modified_at
        self.atomic.metadata.modified_at = now
        self.atomic.rollback()
        self.assertEqual(old_modified_at,self.atomic.metadata.modified_at)
        self.assertLess(self.atomic.metadata.modified_at, now)

    def test_atomic_propagation_checkpoint(self):
        self.atomic.start()
        now = datetime.datetime.now()
        old_modified_at = self.atomic.metadata.modified_at
        self.atomic.metadata.modified_at = now
        self.atomic.checkpoint()
        now2 = datetime.datetime.now()
        self.atomic.metadata.modified_at = now2
        self.atomic.rollback()
        self.assertEqual(now, self.atomic.metadata.modified_at)
        self.assertGreater(now2, self.atomic.metadata.modified_at)
        self.assertLess(old_modified_at, self.atomic.metadata.modified_at)
