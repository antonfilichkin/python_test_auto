"""
Write a function that accepts another function as an argument. Then it
should return such a function, so the every call to initial one
should be cached.
def func(a, b):
    return (a ** b) ** 2
cache_func = cache(func)
some = 100, 200
val_1 = cache_func(*some)
val_2 = cache_func(*some)
assert val_1 is val_2
"""
from collections.abc import Callable


def cache(func: Callable) -> Callable:
    func_cache = {}

    def cached(*args, **kwargs) -> Callable:
        func_id = (func.__name__, tuple(args), frozenset(kwargs))
        if func_id not in func_cache:
            func_cache[func_id] = func(*args, **kwargs)
        return func_cache[func_id]

    return cached
