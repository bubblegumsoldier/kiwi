from collections import namedtuple
from kiwi.database.DataAccessor import DataAccessor

Vote = namedtuple('Vote', 'user post vote')

async def recommend_for(user, with_count=10):
    async with DataAccessor(pool_count=3) as accessor:
        if not await accessor.is_user_known(user):
            await accessor.insert_user(user)
        return await accessor.get_random_unvoted(user, with_count)


async def store_feedback(vote):
    async with DataAccessor(pool_count=3) as accessor:
        vote = Vote(**vote)
        await accessor.insert_vote(vote)
        unvoted = await get_unvoted_count(accessor, vote.user)
        return {'user': vote.user, 'unvoted': unvoted}


async def add_content(posts):
    async with DataAccessor() as accessor:
        filtered_posts = [post['id'] for post in posts]
        await accessor.insert_posts(filtered_posts)
        return {'inserted_count': len(posts)}


async def get_unvoted_count(accessor, user):
    post_count = await accessor.count_posts()
    voted = await accessor.vote_count(user)
    return post_count - voted
