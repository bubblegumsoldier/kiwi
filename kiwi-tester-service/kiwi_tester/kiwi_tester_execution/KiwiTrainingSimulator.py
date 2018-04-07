from kiwi_tester.kiwi_tester_execution.KiwiRequestSender import KiwiRequestSender

import time
import sys

class KiwiTrainingSimulator:
    def __init__(self, config):
        self._config = config

    def start_training(self, training_set):
        print("Simulating {} training elements...".format(len(training_set)))

        from time import sleep
        sys.stdout.write('0%')
        for i, element in enumerate(training_set):
            sys.stdout.write('\r')
            KiwiRequestSender(self._config).send_feedback(element[0], element[1], element[2])
            sys.stdout.write("{0:.0f}%".format(float(i)/float(len(training_set)) * 100))
            sys.stdout.flush()
        sys.stdout.write('\r')
        print("--> Successfully simulated training elements")