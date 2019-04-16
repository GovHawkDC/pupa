import os
import redis

from pupa.scrape.caches.cache import Cache


class Redis(Cache):

    def __init__(self, **kwargs):
        pass

    def get(self, key, **kwargs):
        pass

    def set(self, key, value, **kwargs):
        pass
