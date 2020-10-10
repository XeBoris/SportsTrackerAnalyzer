import os
import json
import xml.etree.ElementTree as ET
import gpxpy
import gpxpy.gpx
import datetime
import hashlib
import pandas as pd

from .db_handler import DataBaseHandler
from .shelve_handler import ShelveHandler

from .blueprint import Blueprint

class Strava():

    def __init__(self):

        #Init the important variables in the beginning
        self.gps_path = None
        self.df = None
        self.track_name = None
        self.obj_gps = {
            "timestamp": [],
            "longitude": [],
            "latitude": [],
            "altitude": []
        }

        #Init the remaining stuff:
        self.bp = Blueprint()

        self._init_database_handler()
        self._empty_gpx_info()

    def _init_database_handler(self):
        # init a database handler here:
        self.db_temp = ShelveHandler()
        self.db_dict = self.db_temp.read_shelve_by_keys(["db_name", "db_type", "db_path", "db_user", "db_hash"])
        if self.db_dict.get("db_hash") is None:
            print("You have to choose as user first")
            return

        self.dbh = DataBaseHandler(db_type=self.db_dict["db_type"])
        self.dbh.set_db_path(db_path=self.db_dict["db_path"])
        self.dbh.set_db_name(db_name=self.db_dict["db_name"])

    def _empty_gpx_info(self):
        self.obj_gps["timestamp"] = []
        self.obj_gps["longitude"] = []
        self.obj_gps["latitude"] = []
        self.obj_gps["altitude"] = []

    def set_gps_path(self, gps_path):
        self.gps_path = gps_path

    def import_strava_gpx(self):

        #Import a single gpx file here:
        self.load_gps()

        beg_branch = int(min(self.df["timestamp"]).replace(tzinfo=datetime.timezone.utc).timestamp()*1000)
        end_branch = int(max(self.df["timestamp"]).replace(tzinfo=datetime.timezone.utc).timestamp()*1000)

        #Load the gpx file and create the branch/track info
        blueprint_session = self.bp.StravaSession()
        blueprint_session["start_time"] = beg_branch
        blueprint_session["end_time"] = end_branch
        blueprint_session["created_at"] = beg_branch
        blueprint_session["updated_at"] = end_branch
        blueprint_session["title"] = self.track_name
        blueprint_session["notes"] = self.track_name
        blueprint_session["start_time_timezone_offset"] = 7200000
        blueprint_session["end_time_timezone_offset"] = 7200000
        blueprint_session["sports_type"] = None
        blueprint_session["source"] = "Strave-GPS"

        if blueprint_session["sports_type"] is None:
            activity = ManualSportMapper()
            blueprint_session["sports_type"] = activity

        # We add a track_hash to each track to make it unique:
        hash_str = f"{blueprint_session.get('start_time')}{blueprint_session.get('end_time')}"
        hash_str = hashlib.md5(hash_str.encode("utf-8")).hexdigest()[0:8]
        blueprint_session["track_hash"] = hash_str

        # We add the user specific hash to the track/branch for identification:
        blueprint_session["user_hash"] = self.db_dict.get("db_hash")

        # dbh.write_branch(db_operation="new", track=rt_json)
        self.dbh.write_branch(db_operation="update",
                         track=blueprint_session,
                         track_hash=hash_str)


        # FIRST LEAF:
        # We create a branch which holds only gps relevant information:
        # gps relevant infomation:
        obj_gps_defintion = ["timestamp", "longitude", "latitude",
                             "altitude"]
        df_sel = self.df[self.df.columns & obj_gps_defintion]

        # Create leaf configuration:
        leaf_config = self.dbh.create_leaf_config(leaf_name="gps",
                                             track_hash=hash_str,
                                             columns=obj_gps_defintion)

        # Write the first leaf:
        r = self.dbh.write_leaf(track_hash=hash_str,
                           leaf_config=leaf_config,
                           leaf=df_sel,
                           leaf_type="DataFrame"
                           )
        if r is True:
            print("First leaf written")
            del df_sel

    def load_gps(self):
        """
        This member function reads in a GPX file from Strava
        - Takes track name
        :return:
        """
        self._read_json(self.gps_path)

        for track in self.gpx.tracks:
            self.track_name = track.name
            for segment in track.segments:
                for point in segment.points:
                    #print(point.latitude, point.longitude, point.elevation, point.time)
                    self.obj_gps["latitude"].append(point.latitude)
                    self.obj_gps["longitude"].append(point.longitude)
                    self.obj_gps["altitude"].append(point.elevation)
                    self.obj_gps["timestamp"].append(point.time)

        self.df = pd.DataFrame(self.obj_gps)
        self.df["timestamp"] = pd.to_datetime(self.df["timestamp"])

    def _read_json(self, fjson):
        """
        A simple private member function for reading a json file
        :param fjson:
        :return:
        """
        gpx_file = open(self.gps_path, 'r')
        tree = ET.parse(self.gps_path)
        root = tree.getroot()
        print(root)

        for i in root:

            for j in i:
                print("d", j.text, j.tag)
        self.gpx = gpxpy.parse(gpx_file)
