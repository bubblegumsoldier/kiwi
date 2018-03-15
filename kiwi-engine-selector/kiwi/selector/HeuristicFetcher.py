from kiwi.config import HEURISICS_CONFIG
import datetime
import importlib

class HeuristicFetcher:
    _heuristics = dict()
    _lastUpdated = None
    def __init__(self):
        pass
    
    def update(self, params):
        """
        params: example
        {
            "user": user
        }
        """
        for key in HEURISICS_CONFIG:
            self.update_heuristic(key, params)
        self._lastUpdated = datetime.datetime.now()

    def update_heuristic(self, heuristic, params):
        module_path = HEURISICS_CONFIG[heuristic]["module"]
        module = importlib.import_module(module_path)
        args = []
        necessary_args = []
        if hasattr(HEURISICS_CONFIG[heuristic], "arguments"):
            necessary_args = HEURISICS_CONFIG[heuristic]["arguments"]
        args = { arg_key: params[arg_key] for arg_key in necessary_args }
        self._heuristics[heuristic] = module.get_heuristic(**args)

    def get_heuristics(self):
        return self._heuristics