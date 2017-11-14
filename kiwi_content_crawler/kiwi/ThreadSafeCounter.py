from threading import RLock


class ThreadSafeCounter(object):
    def __init__(self, required_count, call_when_full):
        self._required_count = required_count
        self._count = 0
        self._callback = call_when_full
        self._lock = RLock()

    def increment(self, value):
        with self._lock:
            self._count += value
            if(self._count >= self._required_count):
                self._callback(self._count)


    def decrement(self, value):
        with self._lock:
            self._count -= value
        
