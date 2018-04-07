from kiwi_tester.kiwi_tester_execution.KiwiRequestSender import KiwiRequestSender

class KiwiContentInitializer:
    def __init__(self, config):
        self._config = config

    def initialize_products(self, products):
        print("Initializing product database on server...")
        KiwiRequestSender(self._config).send_content(products)
        print("--> Successfully initialized product database on server")