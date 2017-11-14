import os
import requests
import json
from flask import (Flask, request)
from extract_posts import (store_posts_and_return_new_ids,
                           store_and_return_new_posts)
from NewPostCounter import NewPostCounter
from PostCache import PostCache

app = Flask(__name__)


@app.route('/')
def index_route():
    client_id = os.environ.get('IMGUR_CLIENT_ID')
    headers = {"Authorization": "Client-ID {}".format(client_id)}

    response = requests.get("https://api.imgur.com/3/gallery/t/aww/3",
                            headers=headers)
    return json.dumps(list(store_and_return_new_posts(response.json()["data"])))



