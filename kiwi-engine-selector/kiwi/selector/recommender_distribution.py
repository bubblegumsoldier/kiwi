from sanic.exceptions import ServerError


async def content(session, recommenders, posts):
    for name, recommender in recommenders.items():
        result = await recommender.push_content(session, posts)
        if result.status != 200:
            raise ServerError('{} error during feedback'.format(name),
                              result.status)


async def feedback(session, recommenders, voting):
    for name, recommender in recommenders.items():
        result = await recommender.send_feedback(session, voting)
        if result.status != 200:
            raise ServerError('''Error during feedback distribution.
                            Recommender: {}'''.format(name),
                              result.status)
