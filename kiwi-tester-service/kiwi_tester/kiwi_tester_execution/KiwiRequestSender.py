import requests
from requests_futures.sessions import FuturesSession
from concurrent.futures import wait
from concurrent.futures import ThreadPoolExecutor
from kiwi_tester.exceptions.ServerError import ServerError


class KiwiRequestSender:
    """
    Singleton implementation
    """
    class __KiwiRequestSender:
        def __init__(self, config=None):
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
            r = requests.post(self._endpoints["content"], json=content_request)

            if r.status_code != requests.codes.ok:
                raise ServerError(
                    "Server returned wrong status code...", r.status_code)

        def send_training(self, chunks, retrain=False):
            session = FuturesSession(
                ThreadPoolExecutor(max_workers=len(chunks)))
            training_requests = self._create_training_payload(chunks, retrain)

            done, _ = wait([session.post(self._endpoints["training"],
                                         json=request) for request in training_requests])
            for r in done:
                if r.result().status_code != requests.codes.ok:
                    raise ServerError(
                        "Server returned wrong status code...", r.result().status_code)

        def send_feedback(self, user, product, rating):
            rating_request = {
                "vote": {
                    "user": user,
                    "post": product,
                    "vote": rating
                }
            }
            r = requests.post(self._endpoints["feedback"], json=rating_request)
            if r.status_code != requests.codes.ok:
                raise ServerError(
                    "Server returned wrong status code...", r.status_code)

        def get_prediction_for_user_and_product(self, user, product):
            url = "{}?user={}&item={}".format(
                self._endpoints["prediction"], user, product)
            r = requests.get(url)
            if r.status_code != requests.codes.ok:
                raise ServerError(
                    "Server returned wrong status code...", r.status_code)
            return r.json()["prediction"], r.json()["recommender"]

        def get_recommendation_for_user(self, user):
            recommendation_request = {
                "user": user,
                "count": 1
            }
            r = requests.get(
                self._endpoints["recommendation"], data=recommendation_request)
            if r.status_code != requests.codes.ok:
                raise ServerError(
                    "Server returned wrong status code...", r.status_code)
            return r.json().recommendations.posts

        def _append_endpoint(self, domain, endpoint):
            if not domain.endswith("/"):
                domain = "{}/".format(domain)
            domain = "{}{}".format(domain, endpoint)
            return domain

        def _create_training_payload(self, chunks, retrain=False):
            if not retrain:
                return [{"votes": chunk, "retrain": False}
                        for chunk in chunks]

            training_requests = [{"votes": chunk, "retrain": False}
                                 for chunk in chunks[:-1]]
            training_requests.append({"votes": chunks[-1], "retrain": True})
            return training_requests

    instance = None

    def __init__(self, config=None):
        if not KiwiRequestSender.instance:
            KiwiRequestSender.instance = KiwiRequestSender.__KiwiRequestSender(
                config)
        else:
            if config is None:
                return
            KiwiRequestSender.instance.config = config

    def __getattr__(self, name):
        return getattr(self.instance, name)
