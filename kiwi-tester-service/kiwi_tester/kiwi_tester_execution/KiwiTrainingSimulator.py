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
        from time import sleep
        #sys.stdout.write('0%')
        i = 0
        while dba.has_next_training():
            c_training = dba.get_next_training()
            #sys.stdout.write('\r')
            
            KiwiRequestSender(self._config).send_feedback(c_training[0], c_training[1], c_training[2])
            
            #sys.stdout.write("{0:.0f}%".format(float(i)/float(size) * 100))
            #sys.stdout.flush()
            i += 1
        #sys.stdout.write('\r')
        print("--> Successfully simulated training elements")