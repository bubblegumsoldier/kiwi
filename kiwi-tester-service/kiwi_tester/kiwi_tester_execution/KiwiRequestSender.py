import requests

from kiwi_tester.exceptions.ServerError import ServerError

class KiwiRequestSender:
    """
    Singleton implementation
    """
    class __KiwiRequestSender:
        def __init__(self, config):
            self._config = config
            self._endpoints = {
                "content": self._append_endpoint(self._config.service_domain, "content"),
                "feedback": self._append_endpoint(self._config.service_domain, "feedback"),
                "recommendation": self._append_endpoint(self._config.service_domain, "recommendation"),
                "prediction": self._append_endpoint(self._config.service_domain, "prediction"),
            }

        def send_content(self, products):
            content_request = {
                "posts": products
            }
            r = requests.post(self._endpoints["content"], data = content_request)
            if r.status_code != requests.codes.ok:
                raise ServerError("Server returned wrong status code...", r.status_code)

        def send_feedback(self, user, product, rating):
            rating_request = {
                "feedback": {
                    "user": user,
                    "post": product,
                    "vote": rating
                }
            }
            r = requests.post(self._endpoints["feedback"], data = rating_request)
            if r.status_code != requests.codes.ok:
                raise ServerError("Server returned wrong status code...", r.status_code)

        def get_prediction_for_user_and_product(self, user, product):
            prediction_request = {
                "user": user,
                "post": product
            }
            r = requests.get(self._endpoints["prediction"], data = prediction_request)
            if r.status_code != requests.codes.ok:
                raise ServerError("Server returned wrong status code...", r.status_code)
            return r.json().prediction

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
    def __init__(self, config):
        if not KiwiRequestSender.instance:
            KiwiRequestSender.instance = KiwiRequestSender.__KiwiRequestSender(config)
        else:
            KiwiRequestSender.instance.config = config

    def __getattr__(self, name):
        return getattr(self.instance, name)