from functools import lru_cache
from typing import Any, Callable

# Simple LRU cache for secrets. TTL can be added for more advanced caching.


def cached_secret(maxsize: int = 128) -> Callable:
    """A decorator to cache secret retrieval results."""

    def decorator(func: Callable) -> Callable:
        @lru_cache(maxsize=maxsize)
        def wrapper(*args, **kwargs) -> Any:
            return func(*args, **kwargs)

        return wrapper

    return decorator
