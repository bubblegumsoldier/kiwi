from asyncio import as_completed
from logging import getLogger


class Collector:
    def __init__(self, count, requesters, callback):
        self.callback = callback
        self.count = count
        self.post_cache = []
        self.requesters = requesters

    async def run_requests(self):
        while not await self._post_count_reached():
            futures = [
                r.request()
                for r
                in self.requesters]
            for future in as_completed(futures):
                posts = await future
                self.post_cache.extend(posts)

    async def _post_count_reached(self):
        if len(self.post_cache) >= self.count:
            if self.post_cache:
                getLogger("root").info("collected %d posts with %d requests.",
                                       len(self.post_cache),
                                       self._get_request_count())
                await self.callback(self.post_cache)
            self.post_cache = []
            return True
        return False

    def _get_request_count(self):
        return sum([requester.page - 1 for requester in self.requesters])
