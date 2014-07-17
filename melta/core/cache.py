from weakref import WeakKeyDictionary, proxy
from pickle import dumps
import gc
from melta.utils.utils import listify
from melta.core.melta_types import istypeof, WeakProxyType


class Monitor():
    def __init__(self):
        self.objects = WeakKeyDictionary()

    def init_monitor_state_for(self, obj):
        return self.is_changed(obj)

    def obj_and_included(self, obj):
        ret = [obj_element for obj_element in self.objects if obj == obj_element]
        included = len(ret) > 0
        real_obj = ret[0] if included else None
        return included, real_obj

    def is_changed(self, obj):
        current_pickle = dumps(obj, -1)
        changed = False
        included, real_obj = self.obj_and_included(obj)
        obj = real_obj if real_obj else obj

        if included:
            obj_compare = self.objects[obj] if istypeof(obj, WeakProxyType) else obj
            changed = current_pickle != self.objects[obj_compare]
        self.objects[obj] = current_pickle
        return changed


class MeltaCache(object):
    """
    Melta cache is a bookkeeping mechanism of MeltaCacheObjects associated with the melta_object id, the CacheObjects
    have the original python object in the enviroment and in case of querying it'll consult this very cache.
    Probably the best idea is to implement a LRU cache for now.
    """

    def __init__(self, schema):
        self.to_object_cache = WeakKeyDictionary()
        self.to_melta_object_cache = WeakKeyDictionary()
        self.schema = schema
        self.monitor = Monitor()

    def add_object(self, melta_object, python_object):
        from melta.utils.utils import is_python_instance

        if is_python_instance(python_object):
            object_weak = proxy(python_object)
            melta_object_weak = proxy(melta_object)

            self.monitor.init_monitor_state_for(python_object)
            self.to_object_cache[melta_object] = object_weak
            self.to_melta_object_cache[python_object] = melta_object_weak

    def _delete_melta_object(self, melta_object):
        configuration = self.schema.get_configuration()
        if configuration.can_remove_on_cascade():
            self.schema.remove_object(melta_object)
            gc.collect()
        else:
            self.to_object_cache.pop(melta_object)


    @listify
    def _get_dirty_values(self):
        for k, v in self.to_object_cache.data.items():
            try:
                v.__class__
            except ReferenceError:
                yield k

    def _clean_unused_references(self):
        removed_objects = self._get_dirty_values()
        for value in removed_objects:
            self._delete_melta_object(value())

    def _check_dirty_object(self):
        for cached_melta_object, python_object in self.to_object_cache.data.items():
            if self.monitor.is_changed(python_object):
                melta_object = cached_melta_object()
                melta_object.syncronize(python_object)

    def update_cache(self):
        self._clean_unused_references()
        self._check_dirty_object()