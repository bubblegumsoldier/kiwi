import os
import json
from threading import Thread
from collections import namedtuple
from functools import partial
from http import HTTPStatus
from flask import (Flask, request)
from kiwi.Collector import Collector
from kiwi.Sender import print_response_json
from kiwi.store_posts import store_posts_continuation

app = Flask(__name__)
# ToDo: Configure logging


@app.route("/new/items", methods=["POST"])
def new_items():
    """
    Parses the request, expexts a json object of form {count, return_url}.
    Returns no content, but will make a request to the given url, once enough
    new content has been requested.
    """
    post_data = request.json
    # ToDo: More thorough validation
    if post_data:
        send = partial(print_response_json,
                       post_data["return_url"])
        store = partial(store_posts_continuation, send)
        collector = Collector(post_data["count"], store)

        Thread(target=collector.run_requests).start()
        return ('', HTTPStatus.ACCEPTED)
    return ('Post data invalid', HTTPStatus.BAD_REQUEST)
