from kiwi_tester.kiwi_tester_execution.KiwiRequestSender import KiwiRequestSender
from kiwi_tester.kiwi_tester_database_access.DatabaseAccessor import DatabaseAccessor

import time
import sys

class KiwiTestingSimulator:
    def __init__(self, config):
        self._config = config
    
    def start_testing(self):
        dba = DatabaseAccessor(self._config)
        rs = KiwiRequestSender(self._config)
        size = dba.get_testing_size()

        print("Simulating {} testing elements...".format(size))

        from time import sleep
        sys.stdout.write('0%')

        i = 0
        while dba.has_next_testing():
            c_testing = dba.get_next_testing()
            sys.stdout.write('\r')
            
            prediction = rs.get_prediction_for_user_and_product(c_testing[0], c_testing[1])
            dba.set_current_testing_prediction(prediction)

            rs.send_feedback(c_testing[0], c_testing[1], c_testing[2])

            sys.stdout.write("{0:.0f}%".format(float(i)/float(size) * 100))
            sys.stdout.flush()
            sleep(0.1)
            i += 1

        sys.stdout.write('\r')
        print("--> Successfully simulated testing elements")