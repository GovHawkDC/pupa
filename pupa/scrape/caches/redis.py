import os
import redis

from pupa.scrape.caches.cache import Cache


class Redis(Cache):

    def __init__(self, **kwargs):
        host = os.environ.get('REDIS_HOST')
        port = os.environ.get('REDIS_PORT')
        password = os.environ.get('REDIS_PASSWORD')
        self.conn = redis.Redis(host=host, port=port, password=password
                                decode_responses=True)

    def get(self, key, **kwargs):
        return self.conn.get(key)

    def set(self, key, value, **kwargs):
        return self.conn.set(key, value)
