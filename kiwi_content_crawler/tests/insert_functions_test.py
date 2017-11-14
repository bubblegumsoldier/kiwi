import unittest

from kiwi.insert_functions import update_post_with_id


class DataStoreTest(unittest.TestCase):
    def test_update_post_with_id(self):
        doc = {"id": 1, "data": "test"}
        modified_doc = update_post_with_id(doc)
        self.assertDictEqual({"_id": 1, "id": 1, "data": "test"}, modified_doc)
        self.assertDictEqual({"id": 1, "data": "test"}, doc)
