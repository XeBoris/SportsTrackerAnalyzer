import json

class Blueprint():
    """
    This class allows us to
    """

    def __init__(self):
        pass

    def manual_sport_mapper(self):
        allowed_activities = ["cycling", "mountainbike", "hiking", "walking"]

        print("Activities are:")
        for i in allowed_activities:
            print(" - ", i)
        print()

        activity = ""
        while activity not in allowed_activities:
            activity = input("State your activity: ")
        print(f"Selected: {activity}")
        return activity

    def _runtastic_sports_mapper(self, nb):
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

    def runtastic_session(self, json_info):
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
        blueprint["sports_type"] = self._runtastic_sports_mapper(json_info.get("sport_type_id"))
        blueprint["source"] = "RTDB"  # Stands for Runtastic Database, no versioning since not observed

        return blueprint

    def runtastic_metadata(self, json_info):
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

    def runtastic_session_lonlat(self, json_info):

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

    def runtastic_session_elevation(self, json_info):
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

    def strava_session(self):
        """

        :param obj:
        :return:
        """
        blueprint = {}
        blueprint["start_time"] = None
        blueprint["end_time"] = None
        blueprint["created_at"] = None
        blueprint["updated_at"] = None
        blueprint["title"] = None
        blueprint["notes"] = None
        blueprint["start_time_timezone_offset"] = None
        blueprint["end_time_timezone_offset"] = None
        blueprint["sports_type"] = None
        blueprint["source"] = "StravaGps"

        return blueprint