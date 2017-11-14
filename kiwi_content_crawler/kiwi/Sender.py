from json import dumps
import requests


def send_response_json(send_url, data):
    requests.post(send_url, json=dumps({"posts": data}))

def print_response_json(send_url, data):
    print(data)
