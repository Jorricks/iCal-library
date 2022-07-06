import functools
import weakref


def instance_lru_cache(*lru_args, **lru_kwargs):
    """
    Add a lru_cache on an instance function without causing a memory leak.
    At the moment you add a standard lru_cache on an instance function (e.g. `def abc(self):`) it counts a reference for
     the python reference counter. This means that when the instance is deleted in the users code, the instance will not
     be collected by the garbage collector because the lru_cache keeps the reference counter for the instance at a
     positive value.
    This implementation prevents this by ensuring the reference to the self attribute is a weak reference. Thereby it is
     not counted in the reference counter and thus can be freely cleared by the garbage collector.
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
