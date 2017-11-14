from threading import (Thread, current_thread)
from PostCache import PostCache
from ThreadSafeCounter import ThreadSafeCounter
from Requester import Requester, Params


DEFINED_TOPICS = ["funny", "aww"]


class Collector(object):
    def __init__(self, count, callback):
        self.callback = callback
        self.post_cache = PostCache(
            ThreadSafeCounter(count, self.post_results))
        self.requesters = [Requester(
            Params(tag=topic, window="week", sort="top"),
            self.post_cache)
            for topic in DEFINED_TOPICS]

        self.threads = [Thread(target=requester.request, args=[1])
                        for requester in self.requesters]

    def run_requests(self):
        for thread in self.threads:
            thread.start()

    def post_results(self, count):
        for requester in self.requesters:
            requester.cancel()

        for thread in self.threads:
            if thread.is_alive() and thread.ident != current_thread().ident:
                return  # other threads should handle callback

        print(count)
        self.callback(self.post_cache.empty())
