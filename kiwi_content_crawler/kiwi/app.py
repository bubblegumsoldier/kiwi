import os
import json
from threading import Thread
from collections import namedtuple
from functools import partial
from http import HTTPStatus
from threading import Thread
import requests
from flask import (Flask, request)
from kiwi.extract_posts import store_and_return_new_posts
from kiwi.Collector import Collector
from kiwi.Sender import print_response_json

app = Flask(__name__)


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
        Thread(target=collector.run_requests).start()
        return ('test', 200)
    
