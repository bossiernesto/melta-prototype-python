from unittest import TestCase
from melta.core.cache import Monitor

class A:
    def __init__(self, number):
        self.number = number


class TestCacheMonitor(TestCase):
    def setUp(self):
        self.a = A(12)
        self.b = A(55)
        self.c = A(4)
        self.monitor = Monitor()
        self.monitor.is_changed(self.a)
        self.monitor.is_changed(self.b)
        self.monitor.is_changed(self.c)

    def test_monitor_not_changed(self):
        self.assertFalse(self.monitor.is_changed(self.a))
        self.b.number = 434
        self.assertFalse(self.monitor.is_changed(self.c))

    def test_changed(self):
        self.assertFalse(self.monitor.is_changed(self.a))
        self.a.number = 23
        self.assertTrue(self.monitor.is_changed(self.a))
        self.assertFalse(self.monitor.is_changed(self.a))

    def test_change_some_objects(self):
        self.assertFalse(self.monitor.is_changed(self.a))
        self.assertFalse(self.monitor.is_changed(self.c))
        self.c.number = 2
        self.assertFalse(self.monitor.is_changed(self.a))
        self.assertTrue(self.monitor.is_changed(self.c))

    def test_change_weakred(self):
        import weakref

        c_weak = weakref.proxy(self.c)
        self.assertFalse(self.monitor.is_changed(self.c))
        self.c.number = 23
        self.assertTrue(self.monitor.is_changed(self.c))
        self.assertFalse(self.monitor.is_changed(self.c))
