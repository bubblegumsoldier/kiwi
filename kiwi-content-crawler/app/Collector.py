from asyncio import as_completed


class Collector:
    def __init__(self, count, requesters, callback):
        self.callback = callback
        self.count = count
        self.post_cache = []
        self.requesters = requesters

    async def run_requests(self):
        print("Starting requests")
        while not await self._post_count_reached():
            futures = [
                r.request()
                for r
                in self.requesters]
            for future in as_completed(futures):
                posts = await future
                print("collected {n} posts".format(n=len(posts)))
                self.post_cache.extend(posts)

    async def _post_count_reached(self):
        if len(self.post_cache) >= self.count:
            await self.callback(self.post_cache)
            self.post_cache = []
            return True
        return False
