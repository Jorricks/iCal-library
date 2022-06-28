import functools
import weakref


def instance_lru_cache(*lru_args, **lru_kwargs):
    """
    The standard lru_cache is not cleared when the instance is deleted. Hence, we use this implementation.
    Inspiration from: https://stackoverflow.com/a/33672499/2277445
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapped_func(self, *args, **kwargs):
            # We're storing the wrapped method inside the instance. If we had
            # a strong reference to self the instance would never die.
            self_weak = weakref.ref(self)
            @functools.wraps(func)
            @functools.lru_cache(*lru_args, **lru_kwargs)
            def cached_method(*args, **kwargs):
                return func(self_weak(), *args, **kwargs)
            return cached_method(*args, **kwargs)
        return wrapped_func
    return decorator