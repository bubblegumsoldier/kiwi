from collections import namedtuple

Voting = namedtuple('Voting', 'user post vote')
Endpoints = namedtuple('Endpoints', 'recommendation feedback content activation')
RecommendationRequest = namedtuple('RecommendationRequest', 'user count')
Response = namedtuple('Response', 'status json')
