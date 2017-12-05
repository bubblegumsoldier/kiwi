import logging
from threading import Thread
from functools import partial
from http import HTTPStatus
from flask import (Flask, request)
from Collector import Collector
from sending import send_response_json
from store_posts import store_posts_continuation
from config import read_config, read_mongo_config


app = Flask(__name__)
requester_config = read_config()


@app.route('/items', methods=['POST'])
def new_items():
    '''
    Parses the request, expexts a json object of form {count, return_url}.
    Returns no content, but will make a request to the given url, once enough
    new content has been requested.
    '''
    post_data = request.json
    if post_data:
        print('received request {!r}'.format(post_data))
        send = partial(send_response_json,
                       post_data['return_url'])
        store = partial(store_posts_continuation, send)
        collector = Collector(post_data['count'], store, requester_config)

        Thread(target=collector.run_requests).start()
        return ('Accepted', HTTPStatus.ACCEPTED)
    return ('Post data invalid', HTTPStatus.BAD_REQUEST)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)