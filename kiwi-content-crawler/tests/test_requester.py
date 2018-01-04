from asynctest import TestCase, MagicMock, CoroutineMock, call
from aiohttp import ClientSession, ClientResponse

from app.Requester import Requester, AUTH_HEADER
from app.PostExtractor import PostExtractor


posts = [
    {'id': 1, 'is_album': False, 'type': 'video/mp4'},
    {'id': 2, 'is_album': False, 'type': 'image/gif'},
    {'id': 3, 'is_album': True},
    {'id': 4, 'is_album': True, 'type': 'image/jpeg'}]

gallery = {'data': {'items': posts}}

url_template = 'test/{tag}/{sort}/{window}/{page}'
path = ('test_tag', 'asc', 'week')

url_temp_with_path_url = 'test/test_tag/asc/week/{}'


async def duplication_predicate(post_id):
    return post_id == 1 or post_id == 3


class TestRequester(TestCase):

    def setUp(self):
        session = MagicMock(ClientSession)
        response = MagicMock(ClientResponse)
        session.get.return_value = response
        response.__aenter__.return_value = response
        response.json.side_effect = CoroutineMock(return_value=gallery)

        extractor = PostExtractor(['video'],
                                  duplication_predicate)

        self.response = response
        self.session = session
        self.requester = Requester(
            session, url_template, path, extractor.extract_and_filter_duplicates)

    async def test_request_one_call(self):
        extracted_posts = await self.requester.request()
        self.assertEqual(extracted_posts, [posts[1]])
        self.response.json.assert_called_once()
        self.session.get.assert_called_once_with(
            url_temp_with_path_url.format(1), headers=AUTH_HEADER)
        self.response.__aenter__.assert_called_once()
        self.response.json.assert_called_once()
        self.response.__aexit__.assert_called_once()

    async def test_request_two_calls(self):
        extracted_posts = await self.requester.request()
        self.session.get.assert_called_with(
            url_temp_with_path_url.format(1), headers=AUTH_HEADER)
        extracted_posts2 = await self.requester.request()
        self.session.get.assert_called_with(
            url_temp_with_path_url.format(2), headers=AUTH_HEADER)
