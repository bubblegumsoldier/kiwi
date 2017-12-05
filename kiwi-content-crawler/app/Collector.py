from concurrent.futures import ThreadPoolExecutor, as_completed
from extract_posts import filter_duplicates
from PostCache import PostCache
from ThreadSafeCounter import ThreadSafeCounter
from Requester import Requester


class Collector:
    def __init__(self, count, callback, requester_config):
        self.callback = callback

        self.post_cache = PostCache(
            ThreadSafeCounter(count, self.post_results))

        self.requesters = [Requester(url=requester_config.url, params=topic)
                           for topic in requester_config.topics]

    def run_requests(self):
        print('starting requests')
        with ThreadPoolExecutor(len(self.requesters)) as executor:
            while True:
                futures = [
                    executor.submit(r.request, filter_duplicates)
                    for r
                    in self.requesters]
                for future in as_completed(futures):
                    posts = list(future.result())
                    print("collected {n} posts".format(n=len(posts)))
                    self.post_cache.append(posts)
                    if self.post_cache.is_empty() and posts:
                        return

    def post_results(self):
        self.callback(self.post_cache.empty())
