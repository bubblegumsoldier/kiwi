from kiwi.database.data_access import (get_random_unvoted, insert_vote,
                                       is_user_known, insert_user, insert_posts)


async def recommend_for(user, with_count=10):
    if not (await is_user_known(user)):
        await insert_user(user)
    return await get_random_unvoted(user, with_count)
    

async def store_feedback(vote):
    await insert_vote(vote)


async def add_content(posts):
    filtered_posts = (post['id'] for post in posts)
    await insert_posts(filtered_posts)
    return filtered_posts

