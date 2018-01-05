from logging import getLogger
from Types import Response


class ContentException(Exception):
    pass


async def content(session, recommenders, posts):
    try:
        for name, recommender in recommenders.items():
            response = await recommender.push_content(session, posts)
            if response.status == 500:
                raise ContentException(
                    "Insernal Server Error for recommender: {name}"
                    .format(name=name))
        return Response(status=200, json={})
    except ContentException as e:
        getLogger("error").error(e)
        return Response(status=500, json={})

async def feedback(session, recommenders, voting):
    for _, recommender in recommenders.items():
        await recommender.send_feedback(session, voting)
