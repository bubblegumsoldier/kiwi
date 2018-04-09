from logging import getLogger
from kiwi.selector.Types import Response
from asyncio import gather

class ContentException(Exception):
    pass


async def content(session, recommenders, posts):
    """
    What happens if the failing recommender is the middle one?
    First one will have received updates, second one errors, third one nothing?
    -> Inconsistent.
    For concistency needs some kind of rollback, but that will likely be difficult to implement.
    Other option: Fail softly? I.e. do not complain on duplicates?
    Also: Could be optimized to start all requests in parallel.
    """

    results = await gather([_content(session, name, recommender, posts) 
            for name, recommender in recommenders])
    return all([True if status == 200 else False for status in results])        

async def feedback(session, recommenders, voting):
    for _, recommender in recommenders.items():
        await recommender.send_feedback(session, voting)


async def _content(session, name, recommender, posts):
    response = await recommender.push_content(session, posts)
    if response.status == 500:
        getLogger("error").error(
            "Internal Server Error for recommender: %s", name)        
    return response.status
