from collections import namedtuple

Vote = namedtuple('Vote', 'user post vote')


def create_vote(vote_dict):
    """
    The movielens algorithm expects integer user and items ids.
    This function adapts the strings in a vote accordingly.
    """
    user = int(vote_dict['user'])
    post = int(vote_dict['post'])
    vote = float(vote_dict['vote'])
    return Vote(user=user, post=post, vote=vote)
