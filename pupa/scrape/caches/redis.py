import os
import redis

from pupa.scrape.caches.cache import Cache


class Redis(Cache):

    def __init__(self, **kwargs):
        host = os.environ.get('REDIS_HOST')
        port = os.environ.get('REDIS_PORT')
        password = os.environ.get('REDIS_PASSWORD')
        self.conn = redis.StrictRedis(host=host, port=port, password=password)

    def get(self, key, **kwargs):
        pass

    def set(self, key, value, **kwargs):
        pass
