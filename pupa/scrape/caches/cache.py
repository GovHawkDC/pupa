from abc import ABCMeta, abstractmethod

class Cache(metaclass=ABCMeta):

    @abstractmethod
    def get(self, key, **kwargs):
        pass

    @abstractmethod
    def set(self, key, value, **kwargs):
        pass
