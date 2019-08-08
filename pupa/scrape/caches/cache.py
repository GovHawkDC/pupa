from abc import ABCMeta, abstractmethod


class Cache(metaclass=ABCMeta):

    def __init__(self, scraper):
        self.scraper = scraper

    @abstractmethod
    def get(self, key, **kwargs):
        pass

    @abstractmethod
    def set(self, key, value, **kwargs):
        pass
