from abc import ABCMeta


class SingletonABCMeta(ABCMeta):
    """Bare-bones singleton ripped from @see https://stackoverflow.com/a/6798042/1858091;
    noticed some of the connection handling code was being run at least twice for some
    of alternative output and cache instances. Although probably not a huge deal, attempting
    to use this as a metaclass to avoid multiple connections, e.g.,

    @see https://stackoverflow.com/a/33364149/1858091 for overcoming inheritance issues

    class MyClass(metaclass=SingletonABCMeta):
        pass
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
