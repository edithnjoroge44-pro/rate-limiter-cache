# Concurrency-safe Rate Limiter + LRU Cache

> **Stack:** Python · threading (thread-safety) · sliding-window algorithm · LRU eviction · pytest
> **Proves:** systems-level **software engineering** — writing thread-safe primitives that back real APIs, and reasoning about concurrency, correctness, and edge cases. This is the "hard systems" skill that clears a senior SWE technical screen.

Two small, battle-tested primitives that every backend service needs:
1. A **sliding-window rate limiter** (per-key, thread-safe, not just a naive counter).
2. An **LRU cache** with O(1) get/put, thread-safe, with correct eviction.

---

## Why these matter
Rate limiting and caching are everywhere in real services. But getting them **concurrency-safe and correct** is the part that trips most candidates. This repo shows:
- **Thread safety** via proper locking (not just a `lock` around everything — correct granularity).
- **Sliding-window** rate limiting that's accurate across time boundaries (not a fixed-reset bug).
- **LRU** with O(1) operations and correct eviction on capacity/access.
- Thorough tests covering concurrent access, boundaries, and eviction.

## Repository structure
```
rate-limiter-cache/
├── README.md
├── requirements.txt
├── ratelimit/
│   ├── limiter.py     # SlidingWindowRateLimiter
│   └── lru.py         # ThreadSafeLRUCache
├── tests/
│   └── test_ratelimit.py
```

## Run it
```bash
pip install -r requirements.txt
pytest tests/ -v
```

## Why it's a strong SWE piece
It demonstrates a deep, transferable engineering skill — concurrency and algorithm correctness — in a small, readable, fully-tested package. A reviewer can read it quickly and see real engineering judgment, not just a scaffold.
