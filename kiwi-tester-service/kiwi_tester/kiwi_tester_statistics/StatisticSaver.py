class StatisticSaver:
    """
    Singleton implementation
    """
    class __StatisticSaver:
        def __init__(self, config):
            self.config = config

        def save_statistic_container(self, container):
            pass
    
    instance = None
    def __init__(self, config):
        if not StatisticSaver.instance:
            StatisticSaver.instance = StatisticSaver.__StatisticSaver(config)
        else:
            StatisticSaver.instance.config = config

    def __getattr__(self, name):
        return getattr(self.instance, name)