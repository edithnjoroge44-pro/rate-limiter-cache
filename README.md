# Concurrency-safe Rate Limiter + LRU Cache

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white) ![Tests](https://img.shields.io/badge/tests-6%20passing-0bad46) ![License](https://img.shields.io/badge/license-MIT-blue) ![pip](https://img.shields.io/badge/pip%20install-e-blue) ![Release](https://img.shields.io/badge/Release-v0.1.0-0b5394)

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

## Install as a package

```bash
pip install https://github.com/edithnjoroge44-pro/rate-limiter-cache/releases/download/v0.1.0/ratelimit_cache-0.1.0-py3-none-any.whl   # official release (no repo needed)
pip install -e .
python -c "from ratelimit.limiter import SlidingWindowRateLimiter"
python -m pytest          # 6 passing tests, incl. a concurrency smoke test
```

Drop it into any service: the limiter is thread-safe, and the LRU cache evicts in O(1).
