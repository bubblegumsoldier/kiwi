import unittest

from kiwi.extract_posts import extract_posts_from_gallery


class DataStoreTest(unittest.TestCase):

    def test_extract_posts_from_gallery(self):
        gallery_response = {"items": [
            {"id": 1, "data": "test", "is_album": True},
            {"id": 2, "data": "test2", "is_album": False}
        ]}
        extracted_posts = extract_posts_from_gallery(gallery_response)

        self.assertEqual([{"id": 2, "data": "test2", "is_album": False}],
                         extracted_posts)
