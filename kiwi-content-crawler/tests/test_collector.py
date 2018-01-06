from functools import partial
from asynctest import TestCase, MagicMock, CoroutineMock, call
from unittest.mock import PropertyMock

from kiwi.Collector import Collector
from kiwi.Requester import Requester


async def create_posts(requester=None):
    if requester:
        type(requester).page = PropertyMock(return_value=requester.page + 1)
    return [{'id': nr} for nr in range(0, 5)]


class TestCollector(TestCase):

    def setUp(self):
        requester1 = MagicMock(Requester)
        requester2 = MagicMock(Requester)
        requester1.request.side_effect = partial(create_posts, requester1)
        requester2.request.side_effect = partial(create_posts, requester2)
        type(requester1).page = PropertyMock(return_value=1)
        type(requester2).page = PropertyMock(return_value=1)
        self.requester1 = requester1
        self.requester2 = requester2

    async def test_collector_one_requester(self):
        print(self.requester1.page)
        collector = Collector(10, [self.requester1])

        posts, max_page = await collector.run_requests()
        expected = await create_posts() + await create_posts()
        self.requester1.request.assert_has_calls([call(), call()])
        self.assertEqual(posts, expected)
        self.assertEqual(max_page, 3)

    async def test_collector_two_requesters(self):
        collector = Collector(
            10, [self.requester1, self.requester2])
        posts, max_page = await collector.run_requests()
        expected = await create_posts() + \
            await create_posts()

        self.requester1.request.assert_called_once()
        self.requester2.request.assert_called_once()
        self.assertEqual(posts, expected)
        self.assertEqual(max_page, 2)

    async def test_collector_performs_no_requests_if_not_required(self):
        collector = Collector(-2,
                              [self.requester1, self.requester2])
        posts, max_page = await collector.run_requests()
        self.requester1.request.assert_not_called()
        self.requester2.request.assert_not_called()
        self.assertEqual(posts, [])
        self.assertEqual(max_page, 1)
