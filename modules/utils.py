"Utilities module"


class LazyDict(dict):
    _lazy_keys = {}

    def __missing__(self, key):
        self._loadLazyKey(key)
        del self._lazy_keys[key]

        return self[key]

    def addLazy(self, key, value):
        self._lazy_keys[key] = value

    def _loadLazyKey(self, key):
        val = self._lazy_keys[key]

        if callable(val):
            val = val()
            self[key] = val

    def load(self):
        for k in self._lazy_keys:
            self._loadLazyKey(k)

        self._lazy_keys = {}

        return self
