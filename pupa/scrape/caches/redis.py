import os
import redis

from pupa.scrape.caches.cache import Cache
from pupa.scrape.connections.manager import get_conn, set_conn


class Redis(Cache):

    def __init__(self, **kwargs):
        c = get_conn('REDIS')

        if c is None:
            host = os.environ.get('REDIS_HOST')
            port = os.environ.get('REDIS_PORT')
            password = os.environ.get('REDIS_PASSWORD')
            c = redis.Redis(host=host, port=port, password=password, decode_responses=True)
            set_conn('REDIS', c)

        self.conn = c

    def get(self, key, **kwargs):
        return self.conn.get(key)

    def set(self, key, value, **kwargs):
        return self.conn.set(key, value)
