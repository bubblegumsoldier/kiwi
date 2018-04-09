from logging import getLogger
from kiwi.selector.Types import Response
from asyncio import gather


async def content(session, recommenders, posts):
    """
    Distribute content across all recommenders.
    If any recommender fails (i.e. not 200), the returned status code will be 500
    """
    results = await gather([_content(session, name, recommender, posts)
                            for name, recommender in recommenders])
    return all([True if status == 200 else False for status in results])


async def feedback(session, recommenders, voting):
    await gather(
        [r.send_feedback(session, voting) for r in recommenders.values()])


async def _content(session, name, recommender, posts):
    response = await recommender.push_content(session, posts)
    if response.status == 500:
        getLogger("error").error(
            "Internal Server Error for recommender: %s during content distribution", name)
    return response.status
