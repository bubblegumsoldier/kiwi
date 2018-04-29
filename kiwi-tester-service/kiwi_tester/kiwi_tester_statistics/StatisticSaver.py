class StatisticSaver:
    """
    Singleton implementation
    """
    class __StatisticSaver:
        def __init__(self, config):
            self.config = config

        def save_statistic_container(self, container):
            with open(self.config.stats_output, "wf") as f:
                f.write(self.evaluation_score_to_text(container))
                f.write("\n")
                f.write(self.execution_time_to_text(container))
                f.write("\n")
                f.write(self.testing_results_to_text(container)) 
            print("==> Successfully saved statistics to file {}".format(self.config.stats_output))

        def evaluation_score_to_text(self, container):
            return "Evaluation: {0:.6g}".format(container.evaluation_score)
        
        def execution_time_to_text(self, container):
            return "Execution started: {}\nExecution ended: {}\n==>{} min, {} s".format(
                str(container.execution_time_start),
                str(container.execution_time_end),
                container.get_execution_duration_in_minutes_and_seconds()[0],
                container.get_execution_duration_in_minutes_and_seconds()[1]
            )

        def testing_results_to_text(self, container):
            lines = ["{};{};{};{};{};{}ms".format(c[0], c[1], c[2], c[3], c[4], c[5]) for c in container.testing_results]
            return "\n".join(lines)
                
    
    instance = None
    def __init__(self, config):
        if not StatisticSaver.instance:
            StatisticSaver.instance = StatisticSaver.__StatisticSaver(config)
        else:
            StatisticSaver.instance.config = config

    def __getattr__(self, name):
        return getattr(self.instance, name)