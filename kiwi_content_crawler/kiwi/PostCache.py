from threading import RLock

class PostCache(object):
    def __init__(self, counter):
        self._counter = counter
        self._post_ids = []
        self._lock = RLock()

    def append(self, posts):
        with self._lock:
            self._post_ids.extend(posts)
            self._counter.increment(len(posts))

    def pop_n(self, count):
        with self._lock:
            first_n, rest = self._post_ids[:count], self._post_ids[count:]
            self._post_ids = rest
            self._counter.decrement(count)
            return first_n

    def empty(self):
        with self._lock:
            content = self._post_ids
            self._post_ids = []
            self._counter.decrement(len(content))
            return content
    
    def is_empty(self):
        return not self._post_ids
