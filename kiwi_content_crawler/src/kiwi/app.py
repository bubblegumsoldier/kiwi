import os
import requests
import json
from threading import Thread
from collections import namedtuple
from functools import partial
from http import HTTPStatus

from flask import (Flask, request)
from extract_posts import store_and_return_new_posts
from Collector import Collector
from Sender import print_response_json

app = Flask(__name__)
Params = namedtuple("Params", "tag sort window page count")


@app.route('/')
def index_route():
    client_id = os.environ.get('IMGUR_CLIENT_ID')
    headers = {"Authorization": "Client-ID {}".format(client_id)}

    response = requests.get("https://api.imgur.com/3/gallery/t/aww/3",
                            headers=headers)
    return json.dumps(
        list(store_and_return_new_posts(response.json()["data"]))
    )


@app.route("/new/items", methods=["POST"])
def new_items():
    """
    Parses the request, expexts a json object of form {count, return_url}.
    Returns no content, but will make a request to the given url, once enough
    new content has been requested.
    """
    post_data = request.json
    if post_data:
        collector = Collector(post_data["count"],
                              partial(print_response_json,
                                      post_data["return_url"]))
        collector.run_requests()
        return ('test', 200)
    
