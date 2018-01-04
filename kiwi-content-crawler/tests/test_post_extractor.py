import asynctest
from app.PostExtractor import PostExtractor


async def duplicate_filter(post_id):
    return post_id == 1 or post_id == 4



class PostExtractorTest(asynctest.TestCase):

    def setUp(self):
        self.extractor = PostExtractor(['video'], duplicate_filter)
        self.posts = [
            {'id': 1, 'is_album': False, 'type': 'video/mp4'},
            {'id': 2, 'is_album': False, 'type': 'image/gif'},
            {'id': 3, 'is_album': True},
            {'id': 4, 'is_album': True, 'type': 'image/jpeg'}]

    async def test_filter_albums_filters_albums(self):

        filtered = list(await self.extractor.filter_albums(self.posts))

        self.assertEqual(filtered, self.posts[0:2])

    async def test_filter_albums_empty_posts(self):
        filtered = list(await self.extractor.filter_albums([]))

        self.assertEqual(filtered, [])

    async def test_filter_albums_throws_key_error(self):
        self.assertAsyncRaises(KeyError, await self.extractor.filter_albums([{}]))

    async def test_match_forbidden_mimetypes(self):
        matches = [await self.extractor.matches_forbidden_mimetypes(post)
                   for post in self.posts]
        self.assertEqual(matches, [True, False, True, False])

    async def test_filter_duplicates(self):
        self.assertEqual(await self.extractor.filter_duplicates(self.posts), [self.posts[1], self.posts[2]])

    async def test_filter_unsupported_formats(self):
        filtered = await self.extractor.filter_unsupported_formats(self.posts)
        self.assertEqual(filtered, self.posts[1:4:2])

    async def test_extract_posts_from_gallery(self):
        gallery_response = {'items': self.posts}
        extracted = await self.extractor.extract_posts_from_gallery(gallery_response)
        self.assertEqual(extracted, [self.posts[1]])

    async def text_extract_and_filter_duplicates(self):
        gallery_response = {'items': self.posts}
        filtered = await self.extractor.extract_and_filter_duplicates(gallery_response)
        self.assertEqual(filtered, [])
