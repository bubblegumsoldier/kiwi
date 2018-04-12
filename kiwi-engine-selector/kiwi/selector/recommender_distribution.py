from logging import getLogger
from kiwi.selector.Types import Response
from asyncio import gather


async def content(session, recommenders, posts):
    """
    Distribute content across all recommenders.
    If any recommender fails (i.e. not 200), the returned status code will be 500
    """
    results = await gather(*[_content(session, name, recommender, posts)
                             for name, recommender in recommenders.items()])
    return all([True if status == 200 else False for status in results])


async def votes(session, recommenders, votes):
    results = await gather(*[r.push_votes(session, votes)
                             for r in recommenders])
    return all([True if status == 500 else False for status in results])



async def feedback(session, recommenders, voting):
    """
    Fire and forget feedback distribution. Not having same rating matrix in each recommender is acceptable. Worst case, users will see some duplicates.
    """
    return await gather(
        *[r.send_feedback(session, voting) for r in recommenders.values()])


async def _content(session, name, recommender, posts):
    response = await recommender.push_content(session, posts)
    if response.status == 500:
        getLogger("error").error(
            "Internal Server Error for recommender: %s during content distribution", name)
    return response.status
