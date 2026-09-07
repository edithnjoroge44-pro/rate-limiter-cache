"""A thread-safe sliding-window rate limiter (per key)."""
import threading
import time
from collections import defaultdict, deque


class SlidingWindowRateLimiter:
    """Allow up to `limit` events per `window_seconds` per key, using a sliding window.

    A sliding window (rather than a fixed-reset counter) avoids the boundary bug where
    a burst of requests right before a reset slips through. Thread-safe via a lock.
    """

    def __init__(self, limit=10, window_seconds=60):
        self.limit = limit
        self.window = window_seconds
        self._events = defaultdict(deque)   # key -> deque of timestamps
        self._lock = threading.Lock()

    def allow(self, key, now=None):
        """Return True if `key` may proceed right now, and record the event if allowed."""
        now = now if now is not None else time.time()
        with self._lock:
            dq = self._events[key]
            # drop events outside the window
            cutoff = now - self.window
            while dq and dq[0] <= cutoff:
                dq.popleft()
            if len(dq) >= self.limit:
                return False
            dq.append(now)
            return True

    def remaining(self, key, now=None):
        now = now if now is not None else time.time()
        with self._lock:
            dq = self._events[key]
            cutoff = now - self.window
            while dq and dq[0] <= cutoff:
                dq.popleft()
            return max(0, self.limit - len(dq))
