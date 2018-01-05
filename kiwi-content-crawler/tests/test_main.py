from unittest import TestCase

from kiwi.main import validate_post_data


class TestValidate(TestCase):

    def test_validate_low_count(self):
        self.assertFalse(validate_post_data({'count': -2, 'return_url': 'test'}))
        