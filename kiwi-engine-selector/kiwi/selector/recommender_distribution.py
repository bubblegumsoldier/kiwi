from sanic.exceptions import ServerError


async def content(session, recommenders, posts):
    for _, recommender in recommenders.items():
        await recommender.push_content(session, posts)


async def feedback(session, recommenders, voting):
    for _, recommender in recommenders.items():
        await recommender.send_feedback(session, voting)
