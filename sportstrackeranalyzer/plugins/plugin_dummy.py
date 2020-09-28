from sportstrackeranalyzer.plugin_handler.plugin_collector import Collector

import pandas as pd
import numpy as np
from geopy.distance import distance as geopy_distance
import math

@Collector
class Plugin_Dummy():
    """
    This is a simple distance plugin to calculate individual time and position
    differences.
    """
    def __init__(self):
        """
        The class init function. This function holds only information
        about the plugin itself. In that way we can always load the plugin
        without initiating further variables and member functions
        """
        self._plugin_config = {
            "module_name": "Plugin_Example",
            "module_dependencies": ["gps"],
            "leaf_name": "example"
        }

    def init(self):
        """
        The "true" init is used here to setup the plugin
        :return: None
        """
        self.data_dict = None
        self.df_result = None
        self.proc_success = False

    def get_result(self):
        """
        Standard function: Return
        :return: Pandas DataFrame or None
        """
        return self.df_result

    def get_processing_success(self):
        return self.proc_success

    def get_plugin_config(self):
        """
        Standard function: Return
        :return: A dictionary with the plugin configuration
        """
        return self._plugin_config

    def set_plugin_data(self, data_dict):
        """
        Standard function: Set the leaf/plugin configuration

        :param data_dict: A dictionary
        :return: -
        """
        self.data_dict = data_dict

    def run(self):
        """
        Standard function: Triggering the processing feature
        of this plugin from the outside.

        :return: -
        """
        #Run individual steps of the data processing:
        self.processer()


    def processer(self):
        """
        The main function which is used in this plugin to process data
        :return:
        """
        #Fetch all important data for calculations:
        gps_data = self.data_dict.get("gps")

        #Implement you code here!