import os
import redis

from pupa.scrape.caches.cache import Cache
from pupa.scrape.connections.singleton import Singleton


class Redis(Cache, metaclass=Singleton):

    def __init__(self, scraper, **kwargs):
        super().__init__(scraper)

        host = os.environ.get('REDIS_HOST')
        port = os.environ.get('REDIS_PORT')
        password = os.environ.get('REDIS_PASSWORD')
        self.conn = redis.Redis(host=host, port=port, password=password, decode_responses=True)

        self.scraper.info('cache checking enabled with redis as target')

    def get(self, key, **kwargs):
        return self.conn.get(key)

    def set(self, key, value, **kwargs):
        return self.conn.set(key, value)
