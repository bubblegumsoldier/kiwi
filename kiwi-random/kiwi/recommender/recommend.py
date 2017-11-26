from kiwi.database.DataAccessor import DataAccessor
from kiwi.Types import Vote


async def recommend_for(user, with_count=10):
    accessor = await DataAccessor.create(pool_count=3)
    if not await accessor.is_user_known(user):
        await accessor.insert_user(user)
    return await accessor.get_random_unvoted(user, with_count)


async def store_feedback(vote):
    accessor = await DataAccessor.create(pool_count=3)
    vote = Vote(**vote)
    await accessor.insert_vote(vote)
    unvoted = await get_unvoted_count(accessor, vote.user)
    return {'user': vote.user, 'unvoted': unvoted}


async def add_content(posts):
    accessor = await DataAccessor.create()
    filtered_posts = [post['id'] for post in posts]
    await accessor.insert_posts(filtered_posts)
    return {'inserted_count': len(posts)}


async def get_unvoted_count(accessor, user):
    post_count = await accessor.count_posts()
    voted = await accessor.vote_count(user)
    return post_count - voted
