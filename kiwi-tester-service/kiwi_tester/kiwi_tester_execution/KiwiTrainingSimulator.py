from kiwi_tester.kiwi_tester_execution.KiwiRequestSender import KiwiRequestSender
from kiwi_tester.kiwi_tester_database_access.DatabaseAccessor import DatabaseAccessor

import time
import sys

class KiwiTrainingSimulator:
    def __init__(self, config):
        self._config = config

    def start_training(self):
        if self._config.skip_training:
            print("-> Skipping Training")
            return
        dba = DatabaseAccessor(self._config)
        size = dba.get_training_size()
        print("Simulating {} training elements...".format(size))
        full_training_data = []
        while dba.has_next_training():
            c_training = dba.get_next_training()
            
            full_training_data.append({
                "user": c_training[0],
                "post": c_training[1],
                "vote": c_training[2]
            })
        
        chunk_size = 1000
        chunks = list(self._chunks(full_training_data, chunk_size))

        print("(Using {} chunks of size ~{})".format(len(chunks), chunk_size))

        for i, c in enumerate(chunks, start=1):
            retrain = True if i == len(chunks) else False 
            sys.stdout.write('\r')
            
            sys.stdout.write("{0:.0f}%".format(float(i)/float(len(chunks)) * 100))
            KiwiRequestSender(self._config).send_training(c, retrain)

            sys.stdout.flush()
        time.sleep(len(chunks))
        sys.stdout.write('\r')

        
        print("--> Successfully simulated training elements")

    def _chunks(self, l, n):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i:i + n]