from abc import abstractmethod

from pupa.scrape.connections.singleton import SingletonABCMeta


class Cache(metaclass=SingletonABCMeta):

    def __init__(self, scraper):
        self.scraper = scraper

    @abstractmethod
    def get(self, key, **kwargs):
        pass

    @abstractmethod
    def set(self, key, value, **kwargs):
        pass
