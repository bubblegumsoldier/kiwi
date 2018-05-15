from logging import getLogger

class PostExtractor:
    def __init__(self, forbidden_types, duplication_predicate):
        self._forbidden_mimetypes = forbidden_types
        self._duplication_predicate = duplication_predicate

    async def extract_and_filter_duplicates(self, gallery_response):
        posts = await self.extract_posts_from_gallery(gallery_response)
        posts = await self.filter_duplicates(posts)
        return await self.transform_tags_for_posts(posts)

    async def extract_posts_from_gallery(self, gallery_response):
        '''
        Extract all posts that are no albums from the API Response.
        '''
        try:
            return await self.filter_unsupported_formats(
                await self.filter_albums(gallery_response['items']))
        except KeyError:
            getLogger('error').error(gallery_response)


    async def filter_albums(self, items):
        return filter(lambda x: x['is_album'] is False, items)

    async def filter_unsupported_formats(self, posts):
        return [post
                for post in posts
                if not await self.matches_forbidden_mimetypes(post)]

    async def matches_forbidden_mimetypes(self, post):
        if 'type' in post:
            return post['type'].startswith(tuple(self._forbidden_mimetypes))
        return True  # No type is also forbidden.

    async def filter_duplicates(self, posts):
        return [post
                for post in posts
                if not await self._duplication_predicate(post['id'])]


    def _transform_tags(self, post):
        changed = [tag['name'] for tag in post['tags']]
        post['tags'] = '|'.join(changed)
        return post
    
    async def transform_tags_for_posts(self, posts):
        return [self._transform_tags(post) for post in posts]