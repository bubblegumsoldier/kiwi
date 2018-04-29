from kiwi_tester.kiwi_tester_execution.KiwiRequestSender import KiwiRequestSender
from kiwi_tester.kiwi_tester_database_access.DatabaseAccessor import DatabaseAccessor

import time
import sys
import datetime

class KiwiTestingSimulator:
    def __init__(self, config, statistic_container):
        self._config = config
        self.statistic_container = statistic_container
    
    def start_testing(self):
        if self._config.skip_testing:
            print("-> Skipping Testing")
            return
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
            
            start_datetime = datetime.datetime.now()
            prediction, recommender = rs.get_prediction_for_user_and_product(c_testing[0], c_testing[1])
            dba.set_current_testing_prediction(prediction)
            end_datetime = datetime.datetime.now()

            time_delta = end_datetime - start_datetime
            ms = time_delta.microseconds
            
            self.statistic_container.add_testing_result(
                c_testing[0], #user
                c_testing[1], #item
                c_testing[2], #vote
                prediction,   #prediction
                recommender,         #recommender
                ms
            )

            rs.send_feedback(c_testing[0], c_testing[1], c_testing[2])

            sys.stdout.write("{0:.0f}%".format(float(i)/float(size) * 100))
            sys.stdout.flush()
            i += 1

        sys.stdout.write('\r')
        print("--> Successfully simulated testing elements")