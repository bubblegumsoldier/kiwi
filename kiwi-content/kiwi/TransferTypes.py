from collections import namedtuple

Vote = namedtuple('Vote', 'user post vote')


def create_vote(vote_dict, cutoff):
    """
    changes the vote to the [-1, 1] range
    """
    modified_vote = 1 if float(vote_dict['vote']) > cutoff else -1
    print(modified_vote, vote_dict['vote'], cutoff)
    return Vote(
        user=vote_dict['user'],
        post=vote_dict['post'],
        vote=modified_vote
    )
