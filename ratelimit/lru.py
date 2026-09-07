"""A thread-safe LRU cache with O(1) get/put and correct eviction."""
import threading
from collections import OrderedDict


class ThreadSafeLRUCache:
    """Least-Recently-Used cache with O(1) get/put, thread-safe.

    Uses an OrderedDict to track access order. On `get`, the key is moved to the most-recent
    end; on overflow, the least-recently-used entry is evicted. A lock makes it safe under
    concurrent access.
    """

    def __init__(self, capacity=128):
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self._data = OrderedDict()
        self._lock = threading.Lock()

    def get(self, key, default=None):
        with self._lock:
            if key not in self._data:
                return default
            self._data.move_to_end(key)   # mark as recently used
            return self._data[key]

    def put(self, key, value):
        with self._lock:
            if key in self._data:
                self._data[key] = value
                self._data.move_to_end(key)
                return
            self._data[key] = value
            if len(self._data) > self.capacity:
                self._data.popitem(last=False)   # evict LRU

    def __len__(self):
        with self._lock:
            return len(self._data)
