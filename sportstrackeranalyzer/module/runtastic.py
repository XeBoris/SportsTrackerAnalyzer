import os
import json
import datetime
import hashlib
import pandas as pd

from .db_handler import DataBaseHandler
from .shelve_handler import ShelveHandler


class Blueprint():
    """
    This class allows us to
    """

    def __init__(self):
        pass

    def RuntasticSportsMapping(self, nb):
        """
        Hand over a number, return a sports type:
        :param nb:
        :return:
        """

        sports_types = {
            "1": "running",
            "2": "alpine-skiing",
            "3": "cycling",
            "4": "mountainbike",
            "7": "hiking",
            "9": "alpine-skiing",
            "15": "indoor cycling",
            "19": "unknown",
            "30": "unknown"
        }
        return sports_types[str(nb)]

    def RuntasticSession(self, json_info):
        """

        :param obj:
        :return:
        """
        blueprint = {}
        blueprint["start_time"] = json_info.get("start_time")
        blueprint["end_time"] = json_info.get("end_time")
        blueprint["created_at"] = json_info.get("created_at")
        blueprint["updated_at"] = json_info.get("updated_at")
        blueprint["title"] = json_info.get("notes")  # In runtastic notation: notes = title
        blueprint["notes"] = json_info.get("notes")
        blueprint["start_time_timezone_offset"] = json_info.get("start_time_timezone_offset")
        blueprint["end_time_timezone_offset"] = json_info.get("end_time_timezone_offset")
        blueprint["sports_type"] = self.RuntasticSportsMapping(json_info.get("sport_type_id"))
        blueprint["source"] = "RTDB"  # Stands for Runtastic Database, no versioning since not observed

        return blueprint

    def RuntasticMetadata(self, json_info):
        """
        Aim: Extract meta data information about the area and weather which
        is included in the database dump

        :param json_info:
        :return:
        """
        blueprint = {}
        blueprint["average_speed"] = json_info.get("average_speed")
        blueprint["calories"] = json_info.get("calories")
        blueprint["longitude"] = json_info.get("longitude")
        blueprint["latitude"] = json_info.get("latitude")
        blueprint["max_speed"] = json_info.get("max_speed")
        blueprint["pause_duration"] = json_info.get("pause_duration")
        blueprint["duration_per_km"] = json_info.get("duration_per_km")
        blueprint["pulse_avg"] = json_info.get("pulse_avg")
        blueprint["pulse_max"] = json_info.get("pulse_max")
        blueprint["avg_cadence"] = json_info.get("avg_cadence")
        blueprint["max_cadence"] = json_info.get("max_cadence")
        blueprint["manual"] = json_info.get("manual")
        blueprint["edited"] = json_info.get("edited")
        blueprint["completed"] = json_info.get("completed")
        blueprint["live_tracking_active"] = json_info.get("live_tracking_active")
        blueprint["live_tracking_enabled"] = json_info.get("live_tracking_enabled")
        blueprint["cheering_enabled"] = json_info.get("cheering_enabled")
        blueprint["indoor"] = json_info.get("indoor")
        blueprint["weather_condition_id"] = json_info.get("weather_condition_id")
        blueprint["surface_id"] = json_info.get("surface_id")
        blueprint["subjective_feeling_id"] = json_info.get("subjective_feeling_id")

        return blueprint

    def RuntasticSessionLonLat(self, json_info):

        blueprint = {}
        # print(len(json_info))

        for i_obj in json_info:
            ts = i_obj["timestamp"]

            blueprint[ts] = {}
            blueprint[ts]["version"] = i_obj["version"]
            blueprint[ts]["longitude"] = i_obj["longitude"]
            blueprint[ts]["latitude"] = i_obj["latitude"]
            blueprint[ts]["altitude"] = i_obj["altitude"]
            blueprint[ts]["accuracy_v"] = i_obj["accuracy_v"]
            blueprint[ts]["accuracy_h"] = i_obj["accuracy_h"]
            blueprint[ts]["speed"] = i_obj["speed"]
            blueprint[ts]["duration"] = i_obj["duration"]
            blueprint[ts]["distance"] = i_obj["distance"]
            blueprint[ts]["elevation_gain"] = i_obj["elevation_gain"]
            blueprint[ts]["elevation_loss"] = i_obj["elevation_loss"]

        return blueprint

    def RuntasticSessionElevation(self, json_info):
        blueprint = {}
        # print(len(json_info))

        for i_obj in json_info:
            ts = i_obj["timestamp"]

            blueprint[ts] = {}
            blueprint[ts]["version"] = i_obj["version"]
            blueprint[ts]["elevation"] = i_obj["elevation"]
            blueprint[ts]["duration"] = i_obj["duration"]
            blueprint[ts]["distance"] = i_obj["distance"]
            blueprint[ts]["elevation_gain"] = i_obj["elevation_gain"]
            blueprint[ts]["elevation_loss"] = i_obj["elevation_loss"]

        return blueprint


class Runtastic():

    def __init__(self):
        self.input_type = None
        self.path = None

        self.path_photos = None
        self.path_purchases = None
        self.path_routes = None
        self.path_sessions = None
        self.path_user = None
        self.path_weight = None

        self.bp = Blueprint()

    def _read_json(self, fjson):
        """
        A simple private member function for reading a json file
        :param fjson:
        :return:
        """
        with open(fjson) as f:
            data = json.load(f)
        return data

    def _get_all_sport_session_ids(self):
        """
        Read all your sport sessions from the available database dump.
        Assume that the <UUID>.json file structure holds for unique
        files. 1 UUID == 1 file == 1 sports activity
        """

        session_ids = []
        for (dirpath, dirnames, filenames) in os.walk(self.path_sessions):
            session_ids.extend(filenames)
            break

        session_ids = [i.replace(".json", "") for i in session_ids]
        return session_ids

    def setup_path(self, type=None, path=None):
        self.input_type = type
        self.path = path
        if type == "database":
            self.path_photos = os.path.join(self.path, "Photos")
            self.path_purchases = os.path.join(self.path, "Purchases")
            self.path_routes = os.path.join(self.path, "Routes")
            self.path_sessions = os.path.join(self.path, "Sport-sessions")
            self.path_user = os.path.join(self.path, "User")
            self.path_weight = os.path.join(self.path, "Weight")

    def get_session_Ids(self):

        if self.input_type == "database":
            return self._get_all_sport_session_ids()

    def _get_rt_db_track_info(self, session_id):
        """
        Get Runtastic Database Track Information

        :param session_id:
        :return:
        """
        pass

    def _read_session_by_id_from_database(self, session_id):
        """
        We will read the Runtastic database dump in

        :param session_id:
        :return:
        """
        # create temporally session path:
        json_path_info = os.path.join(self.path_sessions, f"{session_id}.json")
        json_path_gps = os.path.join(self.path_sessions, "GPS-data", f"{session_id}.json")
        json_path_elv = os.path.join(self.path_sessions, "Elevation-data", f"{session_id}.json")

        # read session info:
        json_info = self._read_json(json_path_info)

        # We will receive meta data from RunTastic First:
        json_info_meta = self.bp.RuntasticMetadata(json_info)

        # We extract timestamps and timestamp names
        dtime = datetime.datetime.utcfromtimestamp(json_info["start_time"] / 1000).strftime('%Y-%m-%dT%H:%M:%SZ')
        dtime_name = datetime.datetime.utcfromtimestamp(json_info["start_time"] / 1000).strftime('%Y-%m-%d-%H-%M')

        # print(dtime, dtime_name)
        # print(json_info)

        # We will receive the main Runtastic information about the track
        json_info = self.bp.RuntasticSession(json_info)

        # We will receive the track (gpx) related information about the track
        # This needs two steps:
        # 1) Read and transform the json objects from database dump (if existing)
        # 2) Merge them into one object with all "raw" information what is available
        # - step 1)
        if os.path.exists(json_path_gps):
            json_gps = self._read_json(json_path_gps)
            data_gps = self.bp.RuntasticSessionLonLat(json_gps)
        else:
            data_gps = {}

        if os.path.exists(json_path_elv):
            json_ele = self._read_json(json_path_elv)
            data_ele = self.bp.RuntasticSessionElevation(json_ele)
        else:
            data_ele = {}
        # - step 2:
        data_gpx_final = []
        if len(data_gps) > 0 and len(data_ele) > 0:
            for key, val in data_gps.items():
                ele = data_ele.get(key)
                if ele is not None:
                    ret = {**val, **ele}
                    ret["timestamp"] = key
                else:
                    ret = val
                    ret["timestamp"] = key

                # adjust timestamp (Move to UTC):
                ret["timestamp"] = datetime.datetime.strptime(ret["timestamp"], '%Y-%m-%d %H:%M:%S %z').timestamp()

                data_gpx_final.append(ret)
        elif len(data_gps) > 0 and len(data_ele) == 0:
            for key, val in data_gps.items():
                ret = val
                ret["timestamp"] = key

                # adjust timestamp (Move to UTC):
                ret["timestamp"] = datetime.datetime.strptime(ret["timestamp"], '%Y-%m-%d %H:%M:%S %z').timestamp()

                data_gpx_final.append(ret)
        elif len(data_gps) == 0 and len(data_ele) == 0:
            pass

        # data_gpx_final #final gpx object
        return {"timestamp": dtime,
                "timestampName": dtime_name,
                "json_info": json_info,
                "json_info_meta": json_info_meta,
                "gpx": data_gpx_final}

    def import_runtastic_sessions(self, overwrite=False):
        """
        You can always import sessions based on the source of runtastic
        Nevertheless, the type is important of how import the sessions

        :return:
        """

        # init a database handler here:
        db_temp = ShelveHandler()
        db_dict = db_temp.read_shelve_by_keys(["db_name", "db_type", "db_path", "db_user", "db_hash"])
        if db_dict.get("db_hash") is None:
            print("You have to choose as user first")
            return

        dbh = DataBaseHandler(db_type=db_dict["db_type"])
        dbh.set_db_path(db_path=db_dict["db_path"])
        dbh.set_db_name(db_name=db_dict["db_name"])

        if self.input_type == "database":
            # This if conditions handles the runtastic database
            # dump as input only:

            # Get all session IDs first:
            all_session_ids = self._get_all_sport_session_ids()

            for session_id in all_session_ids:
                # Extract runtastic relevant data from the database dump
                # and fetch the information from the return object, which is
                # a json object:
                rt_obj = self._read_session_by_id_from_database(session_id)

                # We will handle now several leafs:
                # ---------------------------------

                # We create the branch first from the database dump:
                rt_json = rt_obj.get("json_info")

                # We add a track_hash to each track to make it unique:
                hash_str = f"{rt_json.get('start_time')}{rt_json.get('end_time')}"
                hash_str = hashlib.md5(hash_str.encode("utf-8")).hexdigest()[0:8]
                rt_json["track_hash"] = hash_str

                # We add the user specific hash to the track/branch for identification:
                rt_json["user_hash"] = db_dict.get("db_hash")

                # print(rt_json)

                # dbh.write_branch(db_operation="new", track=rt_json)
                dbh.write_branch(db_operation="update",
                                 track=rt_json,
                                 track_hash=hash_str)

                # Prepare to fill leafs:
                if len(rt_obj.get("gpx")) == 0:
                    continue
                df = pd.DataFrame.from_dict(rt_obj.get("gpx"))

                # FIRST LEAF:
                # We create a branch which holds only gps relevant information:
                # gps relevant infomation:
                obj_gps_defintion = ["timestamp", "longitude", "latitude",
                                     "altitude", "accuracy_v", "accuracy_h",
                                     "version"]
                df_sel = df[df.columns & obj_gps_defintion]

                # Create leaf configuration:
                leaf_config = dbh.create_leaf_config(leaf_name="gps",
                                                     track_hash=hash_str,
                                                     columns=obj_gps_defintion)

                # Write the first leaf:
                r = dbh.write_leaf(track_hash=hash_str,
                                   leaf_config=leaf_config,
                                   leaf=df_sel,
                                   leaf_type="DataFrame"
                                   )
                if r is True:
                    print("First leaf written")
                    del df_sel

                # SECOND LEAF:
                # We create a branch which holds only gps relevant information:
                # gps relevant information:
                obj_gps_defintion = ["timestamp", "speed", "duration",
                                     "distance", "elevation_gain", "elevation_loss",
                                     "elevation", "version"]

                # Select from dataframe:
                df_sel = df[df.columns & obj_gps_defintion]

                # Create leaf configuration:
                leaf_config = dbh.create_leaf_config(leaf_name="runtastic_distances",
                                                     track_hash=hash_str,
                                                     columns=obj_gps_defintion)

                # Write the second leaf:
                r = dbh.write_leaf(track_hash=hash_str,
                                   leaf_config=leaf_config,
                                   leaf=df_sel,
                                   leaf_type="DataFrame"
                                   )
                if r is True:
                    print("Second leaf written")
                    del df_sel

                # Third Leaf: Meta data information:
                # ----------------------------------
                # Extract the json object and put it into a list for the Pandas dataframe:
                rt_metadata = [rt_obj.get("json_info_meta")]
                df_metadata = pd.DataFrame.from_dict(rt_metadata)

                # We do not extract sub information, so take all columns for the object definition
                obj_definition = list(df_metadata.keys())

                # Create leaf configuration:
                leaf_config = dbh.create_leaf_config(leaf_name="runtastic_metadata",
                                                     track_hash=hash_str,
                                                     columns=obj_definition)

                # Write the second leaf:
                r = dbh.write_leaf(track_hash=hash_str,
                                   leaf_config=leaf_config,
                                   leaf=df_metadata,
                                   leaf_type="DataFrame"
                                   )
                if r is True:
                    print("Third leaf written")
                    del df_metadata