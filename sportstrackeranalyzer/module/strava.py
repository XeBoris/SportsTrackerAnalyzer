import os
import json
import datetime
import hashlib
import pandas as pd

from .db_handler import DataBaseHandler
from .shelve_handler import ShelveHandler

class Strava():
    def __init__(self):
        print("init")
        self.gps_path = None

    def set_gps_path(self, gps_path):
        self.gps_path = gps_path

    def load_gps(self):
        print(self.gps_path)
        dt = self._read_json(self.gps_path)
        print(dt)

    def _read_json(self, fjson):
        """
        A simple private member function for reading a json file
        :param fjson:
        :return:
        """
        with open(fjson) as f:
            data = json.load(f)
        return data
