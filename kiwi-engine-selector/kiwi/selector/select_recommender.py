from kiwi.selector.Recommender import Recommender, Voting, Endpoints

# should be read from config
REGISTERED_RECOMMENDERS = {
    'random': Recommender(base_url='http://localhost:8901',
                          endpoints=Endpoints(recommend='recommendation',
                                              feedback='feedback',
                                              content='content'))
}


# somewhere here we need to choose the recommender

# probably shouldnt be async, if we need heavy calculation.
# Maybe run in process pool?
async def choose_recommenders(user):
    # todo

    return REGISTERED_RECOMMENDERS['random']


async def get_pictures(session, user):
    recommender = await choose_recommenders(user)
    pics = await recommender.get_pics_for_user(session, user)
    return pics


async def distribute_content(session, posts):
    for recommender in REGISTERED_RECOMMENDERS.values():
        result = await recommender.push_content(session, posts)
        print(result)
