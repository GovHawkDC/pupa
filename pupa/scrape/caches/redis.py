import os
import redis

from pupa.scrape.caches.cache import Cache


class Redis(Cache):

    _conn = None

    def __init__(self, scraper, **kwargs):
        super().__init__(scraper)

        self.scraper.info('cache checking enabled with redis as target')

        host = os.environ.get('REDIS_HOST')
        port = os.environ.get('REDIS_PORT')
        password = os.environ.get('REDIS_PASSWORD')
        self._conn = redis.Redis(host=host, port=port, password=password,
                                 decode_responses=True)

    def get(self, key, **kwargs):
        return self._conn.get(key)

    def set(self, key, value, **kwargs):
        obj = kwargs.get('obj')
        if obj:
            self.scraper.info('cache %s %s under key %s', obj._type, obj, key)

        return self._conn.set(key, value)
