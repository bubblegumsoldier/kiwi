import requests

from kiwi_tester.exceptions.ServerError import ServerError

class KiwiRequestSender:
    """
    Singleton implementation
    """
    class __KiwiRequestSender:
        def __init__(self, config = None):
            self._config = config
            self._endpoints = {
                "content": self._append_endpoint(self._config.service_domain, "content"),
                "feedback": self._append_endpoint(self._config.service_domain, "feedback"),
                "recommendation": self._append_endpoint(self._config.service_domain, "recommendation"),
                "prediction": self._append_endpoint(self._config.service_domain, "predict"),
                "training": self._append_endpoint(self._config.service_domain, "training")
            }

        def send_content(self, products):
            content_request = {
                "posts": products
            }
            r = requests.post(self._endpoints["content"], json = content_request)
            if r.status_code != requests.codes.ok:
                raise ServerError("Server returned wrong status code...", r.status_code)

        def send_training(self, training, retrain=False):
            training_request = {
                "votes": training,
                "retrain": retrain
            }
            #training should look like this:
            # [{user: "xyz", post: "xyz", vote: "0.1"}, ...]
            r = requests.post(self._endpoints["training"], json = training_request)
            if r.status_code != requests.codes.ok:
                raise ServerError("Server returned wrong status code...", r.status_code)

        def send_feedback(self, user, product, rating):
            rating_request = {
                "vote": {
                    "user": user,
                    "post": product,
                    "vote": rating
                }
            }
            r = requests.post(self._endpoints["feedback"], json = rating_request)
            if r.status_code != requests.codes.ok:
                raise ServerError("Server returned wrong status code...", r.status_code)

        def get_prediction_for_user_and_product(self, user, product):
            url = "{}?user={}&item={}".format(self._endpoints["prediction"], user, product)
            r = requests.get(url)
            if r.status_code != requests.codes.ok:
                raise ServerError("Server returned wrong status code...", r.status_code)
            return r.json()[1]["prediction"]

        def get_recommendation_for_user(self, user):
            recommendation_request = {
                "user": user,
                "count": 1
            }
            r = requests.get(self._endpoints["recommendation"], data = recommendation_request)
            if r.status_code != requests.codes.ok:
                raise ServerError("Server returned wrong status code...", r.status_code)
            return r.json().recommendations.posts
        
        def _append_endpoint(self, domain, endpoint):
            if not domain.endswith("/"):
                domain = "{}/".format(domain)
            domain = "{}{}".format(domain, endpoint)
            return domain

    instance = None
    def __init__(self, config = None):
        if not KiwiRequestSender.instance:
            KiwiRequestSender.instance = KiwiRequestSender.__KiwiRequestSender(config)
        else:
            if config is None:
                return
            KiwiRequestSender.instance.config = config

    def __getattr__(self, name):
        return getattr(self.instance, name)