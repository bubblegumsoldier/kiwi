import unittest

from extract_posts import (extract_posts_from_gallery,
                           filter_duplicates, filter_unsupported_formats)


class DataStoreTest(unittest.TestCase):

    def test_extract_posts_from_gallery(self):
        gallery_response = {"items": [
            {"id": 1, "type": "video/mp4", "is_album": True},
            {"id": 2, "type": "video/mp4", "is_album": False},
            {"id": 3, "type": "video/mpeg", "is_album": False},
            {"id": 4, "is_album": False},
            {"id": 5, "type": "test2", "is_album": False}
        ]}
        forbidden_types = ["video"]
        extracted_posts = extract_posts_from_gallery(
            gallery_response, forbidden_types)

        self.assertEqual(
            [{"id": 5, "type": "test2", "is_album": False}],
            extracted_posts)

    def test_filter_duplicates(self):
        docs = [{"id": 1, "data": "test"}, {"id": 2, "data": "test"}]

        def predicate(x):
            return x is 1

        self.assertEqual(list(filter_duplicates(docs, predicate=predicate)),
                         [docs[1]])

    def test_filter_unsupported_formats(self):
        data = [{"id": 2, "type": "video/mp4", "is_album": False},
                {"id": 3, "type": "video/mpeg", "is_album": False},
                {"id": 4, "is_album": False},
                {"id": 5, "type": "test2", "is_album": False}]
        types = ['video', 'application']
        self.assertEqual(filter_unsupported_formats(data, types),
                         [{"id": 5, "type": "test2", "is_album": False}])
