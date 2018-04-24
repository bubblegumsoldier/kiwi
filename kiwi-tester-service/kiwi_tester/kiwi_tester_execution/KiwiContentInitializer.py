from kiwi_tester.kiwi_tester_execution.KiwiRequestSender import KiwiRequestSender
import sys

class KiwiContentInitializer:
    def __init__(self, config):
        self._config = config

    def initialize_products(self, products):
        if self._config.skip_products:
            print("-> Skipping products")
            return
        print("Initializing product database on server...")
        chunk_size = 1000
        chunks = list(self._chunks(products, chunk_size))
        print("(Using {} chunks of size ~{})".format(len(chunks), chunk_size))

        for i, c in enumerate(chunks, start=1):
            retrain = True if i == len(chunks) else False 
            sys.stdout.write('\r')
            
            sys.stdout.write("{0:.0f}%".format(float(i)/float(len(chunks)) * 100))
            KiwiRequestSender(self._config).send_content(c)

            sys.stdout.flush()
        sys.stdout.write('\r')
        print("--> Successfully initialized product database on server")
    
    def _chunks(self, l, n):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i:i + n]