from sportstrackeranalyzer.plugin_handler.plugin_collector import Collector


@Collector
class Plugin_SimpleDistance():
    def __init__(self):
        #your loader init
        self._plugin_config = {
            "module_name": "Simple_Distance_Calculator",
            "module_dependencies": ["gps"],
            "leaf_name": "simple_distances"
        }

    def init(self):
        #This is your true init
        print("init")

    def get_plugin_config(self):
        return self._plugin_config

    def safe(self):
        pass

    def run(self):
        pass