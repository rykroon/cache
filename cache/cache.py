import pickle
from .connections import get_client

# use 'Undefined' to differentiate between 'None' and 
# the absense of passing in a value.
Undefined = object()


class Cache:

    def __init__(self, key_prefix=None, timeout=Undefined):
        self.key_prefix = key_prefix
        self.timeout = 300 if timeout is Undefined else timeout

    def __contains__(self, key):
        key = self._make_key(key)
        return key in self.client

    @property
    def client(self):
        if not hasattr(self, '_client'):
            self._client = get_client()
        return self._client

    def _make_key(self, key):
        if self.key_prefix:
            return '{}:{}'.format(self.key_prefix, key)
        return key
        
    def get(self, key, default=None):
        key = self._make_key(key)
        value = self.client.get(key)
        if value is None:
            return default
        
        try:
            return pickle.loads(value)
        except pickle.UnpicklingError:
            return value

    def set(self, key, value, timeout=Undefined):
        key = self._make_key(key)
        value = pickle.dumps(value)
        timeout = self.timeout if timeout is Undefined else timeout
        return self.client.set(key, value, ex=timeout)

    def delete(self, key):
        key = self._make_key(key)
        return self.client.delete(key) == 1

    def expire(self, key, timeout=Undefined):
        key = self._make_key(key)
        timeout = self.timeout if timeout is Undefined else timeout
        return self.client.expire(key, timeout)

    def ttl(self, key):
        key = self._make_key(key)
        return self.client.ttl(key)



