
class BaseRecommender:
    def __init__(self, db_connector):
        self._db_connector = db_connector

    def recommend(self, user):
        pass

    
    def integrate_feedback(self, voting):
        pass