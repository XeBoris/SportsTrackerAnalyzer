import os

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