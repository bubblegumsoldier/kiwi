from collections import namedtuple

Voting = namedtuple('Voting', 'user post vote')
Endpoints = namedtuple('Endpoints', 'recommendation feedback content')
User = namedtuple('User', 'name')
Response = namedtuple('Response', 'status json')
