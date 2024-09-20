import json

from redis import Redis


class RedisCache:
    def __init__(self, **kwargs):
        self._redis_client = None
        self.kwargs = kwargs

    def init_app(self, host, port, db, ssl=False, **kwargs):
        self.kwargs.update(kwargs)
        self._redis_client = Redis(host=host, port=port, db=db, ssl=ssl, **self.kwargs)

    def set(self, key, value, expiration=None, only_if_not_exist=False, only_if_exist=False):
        value = json.dumps(value)
        self._redis_client.set(
            name=key, ex=expiration, value=value, nx=only_if_not_exist, xx=only_if_exist
        )
        return True

    def get(self, key):
        value = self._redis_client.get(key)
        return json.loads(value) if value else None

    def delete(self, *keys):
        self._redis_client.delete(*keys)


redis_cache = RedisCache()
