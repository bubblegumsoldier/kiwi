from kiwi_tester.kiwi_tester_execution.KiwiRequestSender import KiwiRequestSender
from kiwi_tester.kiwi_tester_database_access.DatabaseAccessor import DatabaseAccessor

import time
import sys

class KiwiTrainingSimulator:
    def __init__(self, config):
        self._config = config

    def start_training(self):
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
        KiwiRequestSender(self._config).send_training(full_training_data)
        
        print("--> Successfully simulated training elements")