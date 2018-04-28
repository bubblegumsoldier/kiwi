import datetime, sys
class StatisticContainer:
    def __init__(self, init_start_time = True):
        if init_start_time:
            self.execution_time_start = datetime.datetime.now()
        
        self.execution_time_end = None
        self.testing_results = []
        self.evaluation_score = sys.maxsize
    
    def set_evaluation_score(self, score):
        self.evaluation_score = score
    
    def add_testing_result(self, user, item, vote, prediction, recommender, duration):
        self.testing_results.append(tuple(user, item, vote, recommender, duration))
        
    def log_execution_end(self):
        self.execution_time_end = datetime.datetime.now()
    
    def get_execution_duration_in_seconds(self):
        delta = self.execution_time_end - self.execution_time_start
        seconds = delta.timedelta()
        return seconds

    def get_execution_duration_in_minutes_and_seconds(self):
        return divmod(self.get_execution_duration_in_seconds(), 60)