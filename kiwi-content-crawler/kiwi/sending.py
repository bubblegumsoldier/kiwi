import requests


def send_response_json(send_url, data):
    requests.post(send_url, json={'posts': data})


def print_response_json(send_url, data):
    print([post['id'] for post in data])
