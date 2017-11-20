from kiwi.database.data_access import get_random_unvoted, insert_vote


async def recommend_for(user):
    return await get_random_unvoted(user)



async def store_feedback(vote):
    await insert_vote(vote)
