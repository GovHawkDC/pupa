import os
import redis

from pupa.scrape.caches.cache import Cache


class Redis(Cache):

    def __init__(self, **kwargs):
        host = os.environ.get('REDIS_HOST')
        port = os.environ.get('REDIS_PORT')
        password = os.environ.get('REDIS_PASSWORD')
        self.conn = redis.Redis(host=host, port=port, password=password)

    def get(self, key, **kwargs):
        # NOTE: The redis client returns UTF-8 encoded strings, so this is a
        # workaround to convert the stored value, if present and an encoded
        # string, to just a plain old string for comparison
        #
        # E.g., `b'bar' == 'bar' # False`
        #
        # For not using `decode_responses` keyword arg in connection, @see:
        # https://stackoverflow.com/questions/25745053\
        #     /about-char-b-prefix-in-python3-4-1-client-connect-to-redis\
        #     #comment40254650_25745110
        value = self.conn.get(key)
        if value is None:
            return value
        # @see https://stackoverflow.com/a/34870210/1858091
        try:
            return value.decode('utf-8')
        except Exception:
            return value

    def set(self, key, value, **kwargs):
        return self.conn.set(key, value)
