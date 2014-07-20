from unittest import TestCase, skip
from melta.core.basicmodel import AtomicObject, AggregationObject, ReferenceObject
from melta.core.metadata import CLEAN_MELTAOBJECT_STATUS,DIRTY_MELTAOBJECT_STATUS,INVALID_MELTAOBJECT_STATUS

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
        dirty = DIRTY_MELTAOBJECT_STATUS
        clean = self.atomic.metadata.object_status
        self.atomic.metadata.object_status = dirty
        self.atomic.commit()
        self.assertEqual(self.atomic.metadata.object_status, dirty)
        self.assertNotEqual(self.atomic.metadata.object_status, clean)

    def test_atomic_propagation_rollback(self):
        self.atomic.start()
        dirty = DIRTY_MELTAOBJECT_STATUS
        old_status = self.atomic.metadata.object_status
        self.atomic.metadata.object_status = dirty
        self.atomic.rollback()
        self.assertEqual(old_status,self.atomic.metadata.object_status)
        self.assertNotEqual(self.atomic.metadata.object_status, dirty)

    def test_atomic_propagation_checkpoint(self):
        self.atomic.start()
        dirty = DIRTY_MELTAOBJECT_STATUS
        clean = self.atomic.metadata.object_status
        self.atomic.metadata.object_status = dirty
        self.atomic.checkpoint()
        invalid = INVALID_MELTAOBJECT_STATUS
        self.atomic.metadata.object_status = invalid
        self.atomic.rollback()
        self.assertEqual(dirty, self.atomic.metadata.object_status)
        self.assertNotEqual(invalid, self.atomic.metadata.object_status)
        self.assertNotEqual(clean, self.atomic.metadata.object_status)
