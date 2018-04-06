class DatabaseAccessor:
    class __DatabaseAccessor:
        def __init__(self, config):
            self.config = config
        
        def initialize_database(self, training_set, testing_set):
            self.training_set = training_set
            self.testing_set = testing_set

        

        def has_next_training(self):
            if self.last_training_id is None:
                self.last_training_id = -1
            return self.last_training_id + 1 < len(self.training_set) + 1
        
        def get_next_training(self):
            if not self.has_next_training():
                return None
            self.training_set += 1
            return self.training_set[self.last_training_id]
        
        def has_next_testing(self):
            if self.last_testing_id is None:
                self.last_testing_id = -1
            return self.last_testing_id + 1 < len(self.testing_set) + 1
        
        def get_next_testing(self):
            if not self.has_next_testing():
                return None
            self.testing_set += 1
            return self.testing_set[self.last_testing_id]

        def set_current_testing_prediction(self, prediction):
            self.testing_set[self.last_testing_id][3] = prediction
    
    instance = None
    def __init__(self, config):
        if not DatabaseAccessor.instance:
            DatabaseAccessor.instance = DatabaseAccessor.__DatabaseAccessor(config)
        else:
            DatabaseAccessor.instance.config = config
            
    def __getattr__(self, name):
        return getattr(self.instance, name)