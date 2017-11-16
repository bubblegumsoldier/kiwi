from kiwi.selector.Recommender import Recommender, Voting, Endpoints

# should be read from config
REGISTERED_RECOMMENDERS = {
    'random': Recommender(base_url='localhost:7000',
                          endpoints=Endpoints(pics='/new/items', feedback='feedback'))
}



#somewhere here we need to choose the recommender

#probably shouldnt be async, if we need heavy calculation.
# Maybe run in executor
async def choose_recommenders(user):
    #todo

    return REGISTERED_RECOMMENDERS['random']



async def get_pictures(session, user):
    recommender = await choose_recommenders(user)
    pics = await recommender.get_pics_for_user(session, user)
    return pics



