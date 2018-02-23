from collections import namedtuple

Vote = namedtuple('Vote', 'user post vote')


def create_vote(vote_dict):
    """
    The movielens algorithm expects integer user and items ids.
    This function adapts the strings in a vote accordingly.
    """
    return Vote(**vote_dict)
