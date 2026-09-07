import sys, os, threading, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ratelimit.limiter import SlidingWindowRateLimiter
from ratelimit.lru import ThreadSafeLRUCache


def test_rate_limiter_allows_up_to_limit():
    rl = SlidingWindowRateLimiter(limit=3, window_seconds=60)
    assert [rl.allow("user") for _ in range(3)] == [True, True, True]
    assert rl.allow("user") is False   # 4th blocked


def test_rate_limiter_sliding_window_clears_after_window():
    rl = SlidingWindowRateLimiter(limit=1, window_seconds=60)
    assert rl.allow("k", now=0) is True
    assert rl.allow("k", now=10) is False
    # after the window passes, allowed again
    assert rl.allow("k", now=61) is True


def test_rate_limiter_streams_spread_out():
    rl = SlidingWindowRateLimiter(limit=2, window_seconds=60)
    assert rl.allow("k", now=0) is True
    assert rl.allow("k", now=30) is True
    assert rl.allow("k", now=59) is False
    assert rl.allow("k", now=61) is True   # first event (t=0) now outside window


def test_lru_evicts_least_recently_used():
    c = ThreadSafeLRUCache(capacity=2)
    c.put("a", 1); c.put("b", 2)
    c.get("a")            # touch 'a' -> b becomes LRU
    c.put("c", 3)         # evicts 'b'
    assert c.get("a") == 1
    assert c.get("b") is None
    assert c.get("c") == 3


def test_lru_get_moves_to_recent():
    c = ThreadSafeLRUCache(capacity=2)
    c.put("x", 1); c.put("y", 2)
    c.get("x")            # x now most recent
    c.put("z", 3)         # evicts 'y'
    assert c.get("x") == 1
    assert c.get("y") is None


def test_lru_thread_safety_smoke():
    c = ThreadSafeLRUCache(capacity=8)
    errors = []

    def worker(n):
        try:
            for i in range(n):
                c.put(("k", i), i)
                c.get(("k", i))
        except Exception as e:
            errors.append(e)

    threads = [threading.Thread(target=worker, args=(200,)) for _ in range(8)]
    [t.start() for t in threads]
    [t.join() for t in threads]
    assert not errors
    assert len(c) <= 8
