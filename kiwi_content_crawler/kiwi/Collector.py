from concurrent.futures import ThreadPoolExecutor, as_completed
from kiwi.mongo_functions import insert_posts_filter_duplicates
from kiwi.PostCache import PostCache
from kiwi.ThreadSafeCounter import ThreadSafeCounter
from kiwi.Requester import Requester, Params


DEFINED_TOPICS = ["funny", "aww"]


class Collector(object):
    def __init__(self, count, callback):
        self.callback = callback
        self.post_cache = PostCache(
            ThreadSafeCounter(count, self.post_results))
        self.requesters = [Requester(
            Params(tag=topic, window="week", sort="top"))
            for topic in DEFINED_TOPICS]

    def run_requests(self):
        with ThreadPoolExecutor(len(DEFINED_TOPICS)) as executor:
            while True:
                futures = [executor.submit(r.request) for r in self.requesters]

                for future in as_completed(futures):
                    posts = list(
                        insert_posts_filter_duplicates(future.result()))
                    self.post_cache.append(posts)
                    if self.post_cache.is_empty() and posts:
                        return

    def post_results(self, count):
        self.callback(self.post_cache.empty())
