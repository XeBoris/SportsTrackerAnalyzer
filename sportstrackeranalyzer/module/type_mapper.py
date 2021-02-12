import json
import os
import sportstrackeranalyzer as sta

class TypeMapper(object):
    """
    This class introduces a general way to describe sport types
    across different data sources such as runtastic, strava or
    general gps files.
    The general idea is to give users a way to describe sport
    types from this class with the help of a configuration file
    which is shipped out with the package.
    """
    def __init__(self):
        """
        Constructor
        """
        self._basic_path = sta.__path__[0]

        self._track_source = None
        self._track_sources = None #path
        self._source_type = None

        self._basic_mapper = None  # Hold the basic maps (JSON)
        self._track_source_mapper = None

    def set_track_source(self, track_source=None):
        """
        Allow a user to set the path manually. This path
        describes the mapper types between the basic types (see basic_mapper)
        and the sport types from the third parity applications (e.g. Strava)
        :param track_source: An absolute path to a map file.
        :return: None
        """
        self._track_source = track_source

    def set_source_type(self, source_type=None):
        """
        Allow a user to set the path manually. This path
        describes the mapper types between third parity apps (e.g. Strava)
        and the basic sport types which are used in STA. These sport types
        are listed in the branches later.
        :param source_type: An absolute path to a map file.
        :return: None
        """
        self._source_type = source_type

    def _load_basic_mapper(self):
        """
        If no manual adjustments are done to the paths, the basic sport mapper
        and third parity mapper is loaded from the installation path. Therefore
        this function loads the path.
        :return: None
        """
        if self._source_type is None:
            self.types = f"{self._basic_path}/configuration/basic_types.config"
        else:
            print("Specify basic mapper file manually.")
        if os.path.exists(self.types):
            with open(self.types) as json_file:
                self._basic_mapper = json.load(json_file)

    def _load_track_source(self):
        """
        If no manual adjustments are done to the paths, the basic sport mapper
        and third parity mapper is loaded from the installation path. Therefore
        this function loads the path.
        :return: None
        """
        if self._track_sources is None:
            self._track_sources = f"{self._basic_path}/configuration/type_mapper.config"
        else:
            print("Specify Sports mapper")

        if os.path.exists(self._track_sources):
            with open(self._track_sources) as json_file:
                self._track_source_mapper = json.load(json_file)
        self._track_source_mapper = self._track_source_mapper.get(self._track_source)

    def loader(self):
        """
        Once the path are set in whatever way, you are welcome to load the files.
        :return: None
        """
        self._load_track_source()
        self._load_basic_mapper()

    def mapper(self, _id):
        """
        The mapper(...) connect the third parity sport types wiith the basic sport types.
        Once the class perquisite are setup correctly, just use this member function to
        get your mapping done correctly.
        :param _id: A number or string to describe the third parity sport type
        :return: A string that describe the sport type in our branches.
        """
        try:
            m = [i for i in self._track_source_mapper if i["id"] == str(_id)][0]
            map_type = m.get("map_types")
        except IndexError as e:
            map_type = "0"

        s_type = self._basic_mapper.get("types").get(map_type)
        return s_type