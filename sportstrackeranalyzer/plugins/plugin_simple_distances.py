from sportstrackeranalyzer.plugin_handler.plugin_collector import Collector

import pandas as pd
import numpy as np
from geopy.distance import distance as geopy_distance
from geopy.distance import geodesic as geopy_geodesic
from geopy.distance import great_circle as geopy_greatcircle
import math

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
        self.data_dict = None
        self.df_result = None
        self.proc_success = False

    def get_result(self):
        return self.df_result

    def get_processing_success(self):
        return self.proc_success

    def get_plugin_config(self):
        return self._plugin_config

    def set_plugin_data(self, data_dict):
        self.data_dict = data_dict

    def run(self):
        #Run individual steps of the data processing:
        self.processer()


    def processer(self):

        #Fetch all important data for calculations:
        gps_data = self.data_dict.get("gps")

        # Your calculations start here:
        #collecter:
        dt_list = []
        dx_list = []
        dxz_list = []

        gps0 = None
        time0 = None

        for row in gps_data.T.iteritems():
            # Extract the first row
            i_gps = (row[1]["latitude"], row[1]["longitude"], row[1]["altitude"])
            i_time = row[1]["timestamp"]

            # Set the gps/time to zero
            if gps0 is None:
                gps0 = i_gps
            if time0 is None:
                time0 = i_time

            # time difference:
            #dt = (i_time - time0).total_seconds()
            dt = (i_time - time0)

            # geodasic distance (x/y)
            dx = geopy_distance(i_gps[:2], gps0[:2]).m

            # Euclidian distance
            dxz = math.sqrt(dx ** 2 + (i_gps[2] - gps0[2]) ** 2)

            dt_list.append(dt)
            dx_list.append(dx)
            dxz_list.append(dxz)

            gps0 = i_gps
            time0 = i_time

        dt_cumsum_list = np.cumsum(dt_list)
        dx_cumsum_list = np.cumsum(dx_list)
        dxz_cumsum_list = np.cumsum(dxz_list)

        dv_geodasic = [i / j if j > 0 else 0 for i, j in zip(dx_list, dt_list)]
        dv_euclidian = [i / j if j > 0 else 0 for i, j in zip(dxz_list, dt_list)]

        # Extract information from the calculations for the final dataframe:
        results = {
            'duration': dt_list,
            'duration_sum': dt_cumsum_list,
            'dist_geodasic': dx_list,
            'dist_euclidiac': dxz_list,
            'dist_geodasic_sum': dx_cumsum_list,
            'dist_euclidiac_sum': dxz_cumsum_list,
            'velocity_geodasic': dv_geodasic,
            'velocity_euclidic': dv_euclidian
        }

        self.df_result = pd.DataFrame(data=results)

        #if you make it to here:
        self.proc_success = True