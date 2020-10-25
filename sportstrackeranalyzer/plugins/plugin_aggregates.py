from sportstrackeranalyzer.plugin_handler.plugin_collector import Collector

import pandas as pd
import numpy as np
from geopy.distance import distance as geopy_distance
import math

@Collector
class Plugin_SimpleProjection():
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
            "module_name": "Simple_Projection",
            "module_dependencies": ["simple_distances", "gps"],
            "leaf_name": "simple_projection"
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
        sdistances = self.data_dict.get("simple_distances")
        sgps = self.data_dict.get("gps")

        final = {"tot_dist_geodasic": [sdistances["dist_geodasic"].sum()],
                 "tot_dist_euclidiac": [sdistances["dist_euclidiac"].sum()],
                 "tot_duration": [sdistances["duration"].sum()],
                 "median_velocity_geodasic": [sdistances["velocity_geodasic"].median()],
                 "mean_velocity_geodasic": [sdistances["velocity_geodasic"].mean()],
                 "median_velocity_euclidic": [sdistances["velocity_euclidic"].median()],
                 "mean_velocity_euclidic": [sdistances["velocity_euclidic"].mean()]
                 }

        sgps["altitudeDiff"] = sgps["altitude"].shift(1) - sgps["altitude"]

        #print(sgps["altitudeDiff"].to_list())
        # self.df_result = pd.DataFrame(data=results)
        pos = sgps[(sgps["altitudeDiff"] > 0)]
        neg = sgps[(sgps["altitudeDiff"] < 0)]
        pos_sum = pos["altitudeDiff"].sum()
        neg_sum = neg["altitudeDiff"].sum()
        final["altitude_up"] = [pos_sum]
        final["altitude_dw"] = [neg_sum]

        final["max_velocity_geodasic"] = [sdistances["velocity_geodasic"].describe()["max"]]
        final["m75p_velocity_geodasic"] = [sdistances["velocity_geodasic"].describe()["75%"]]
        final["m50p_velocity_geodasic"] = [sdistances["velocity_geodasic"].describe()["50%"]]
        final["m25p_velocity_geodasic"] = [sdistances["velocity_geodasic"].describe()["25%"]]
        final["min_velocity_geodasic"] = [sdistances["velocity_geodasic"].describe()["min"]]
        final["std_velocity_geodasic"] = [sdistances["velocity_geodasic"].describe()["std"]]
        #final["mean_velocity_geodasic"] = [sdistances["velocity_geodasic"].describe()["mean"]]

        final["max_velocity_euclidic"] = [sdistances["velocity_euclidic"].describe()["max"]]
        final["m75p_velocity_euclidic"] = [sdistances["velocity_euclidic"].describe()["75%"]]
        final["m50p_velocity_euclidic"] = [sdistances["velocity_euclidic"].describe()["50%"]]
        final["m25p_velocity_euclidic"] = [sdistances["velocity_euclidic"].describe()["25%"]]
        final["min_velocity_euclidic"] = [sdistances["velocity_euclidic"].describe()["min"]]
        final["std_velocity_euclidic"] = [sdistances["velocity_euclidic"].describe()["std"]]
        #final["mean_velocity_geodasic"] = [sdistances["velocity_geodasic"].describe()["mean"]]

        self.df_result = pd.DataFrame(data=final)

        print(self.df_result)
        # if you make it to here:
        self.proc_success = True