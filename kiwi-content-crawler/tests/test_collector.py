from asynctest import TestCase, MagicMock, CoroutineMock, call
from unittest.mock import PropertyMock
from kiwi.Collector import Collector
from kiwi.Requester import Requester


async def create_posts(count=5):
    return [{'id': nr} for nr in range(0, count)]


class TestCollector(TestCase):

    def setUp(self):
        requester1 = MagicMock(Requester)
        requester2 = MagicMock(Requester)

        requester1.request.side_effect = create_posts
        requester2.request.side_effect = create_posts

        callback = CoroutineMock()

        self.requester1 = requester1
        self.requester2 = requester2
        self.callback = callback

    async def test_collector_one_requester(self):
        collector = Collector(10, [self.requester1], self.callback)

        await collector.run_requests()
        expected = await create_posts() + await create_posts()
        self.callback.assert_called_once_with(expected)
        self.requester1.request.assert_has_calls([call(), call()])

    async def test_collector_two_requesters(self):
        collector = Collector(
            20, [self.requester1, self.requester2], self.callback)
        await collector.run_requests()
        expected = await create_posts() + \
            await create_posts() + \
            await create_posts() + \
            await create_posts()

        self.callback.assert_called_once_with(expected)
        self.requester1.request.assert_called()
        self.requester2.request.assert_called()

    async def test_collector_performs_no_requests_if_not_required(self):
        collector = Collector(-2,
                              [self.requester1, self.requester2],
                              self.callback)
        await collector.run_requests()

        self.callback.assert_not_called()
        self.requester1.request.assert_not_called()
        self.requester2.request.assert_not_called()
