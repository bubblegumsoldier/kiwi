from asyncio import as_completed
from logging import getLogger
from copy import deepcopy


class Collector:
    def __init__(self, count, requesters):
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
        result = self.post_cache.copy()
        self.post_cache = []
        return (result, max(self._get_pages()))

    async def _post_count_reached(self):
        if len(self.post_cache) >= self.count:
            if self.post_cache:
                pages = self._get_pages()
                getLogger("root").info("collected %d posts",
                                       len(self.post_cache))
            return True
        return False

    def _get_pages(self):
        return [requester.page for requester in self.requesters]
