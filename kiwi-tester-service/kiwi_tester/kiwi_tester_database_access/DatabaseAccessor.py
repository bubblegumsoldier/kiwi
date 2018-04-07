class DatabaseAccessor:
    """
    Singleton implementation
    """
    class __DatabaseAccessor:
        def __init__(self, config):
            self.config = config
            self.last_training_id = -1
            self.last_testing_id = -1
        
        def initialize_database(self, training_set, testing_set):
            self.training_set = training_set
            self.testing_set = testing_set

        def get_training_size(self):
            return len(self.training_set)

        def has_next_training(self):
            return self.last_training_id + 1 < len(self.training_set)
        
        def get_next_training(self):
            if not self.has_next_training():
                return None
            self.last_training_id += 1
            return self.training_set[self.last_training_id]

        def get_testing_size(self):
            return len(self.testing_set)

        def has_next_testing(self):
            if self.last_testing_id is None:
                self.last_testing_id = -1
            return self.last_testing_id + 1 < len(self.testing_set)
        
        def go_to_first_testing(self):
            self.last_testing_id = -1

        def get_next_testing(self):
            if not self.has_next_testing():
                return None
            self.last_testing_id += 1
            return self.testing_set[self.last_testing_id]

        def set_current_testing_prediction(self, prediction):
            old_t = self.testing_set[self.last_testing_id]
            self.testing_set[self.last_testing_id] = (old_t[0], old_t[1], old_t[2], prediction)
    
    instance = None
    def __init__(self, config):
        if not DatabaseAccessor.instance:
            DatabaseAccessor.instance = DatabaseAccessor.__DatabaseAccessor(config)
        else:
            DatabaseAccessor.instance.config = config

    def __getattr__(self, name):
        return getattr(self.instance, name)