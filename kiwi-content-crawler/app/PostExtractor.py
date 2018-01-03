
class PostExtractor:
    def __init__(self, forbidden_types, duplication_predicate):
        self._forbidden_mimetypes = forbidden_types
        self._duplication_predicate = duplication_predicate

    async def extract_and_filter_duplicates(self, gallery_response):
        posts = await self.extract_posts_from_gallery(gallery_response)
        return await self.filter_duplicates(posts)

    async def extract_posts_from_gallery(self, gallery_response):
        '''
        Extract all posts that are no albums from the API Response.
        '''
        return await self.filter_unsupported_formats(
            await self.filter_albums(gallery_response['items']),
            self._forbidden_mimetypes)

    async def filter_albums(self, items):
        def predicate(x):
            return x['is_album'] is False
        return filter(predicate, items)

    async def filter_unsupported_formats(self, posts, formats):
        async def predicate(x):
            return not await self.matches_forbidden_mimetypes(x, formats)
        return [post for post in posts if await predicate(post)]

    async def matches_forbidden_mimetypes(self, post, types):
        if 'type' in post:
            return post['type'].startswith(tuple(types))
        return True  # No type is also forbidden.

    async def filter_duplicates(self, posts, predicate=None):
        '''
        Filters all duplicate posts. 
        :param predicate:   Predicate to check for duplication. If 'None', the                      default predicate of the object will be used.
        '''
        if not predicate:
            predicate = self._duplication_predicate
        return [post for post in posts if not await predicate(post['id'])]
