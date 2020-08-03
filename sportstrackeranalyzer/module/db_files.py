import os
import uuid
import json
import hashlib

class FileDataBase(object):
    """

    """
    def __init__(self):
        self._db_path = None
        self._db_name = None

    def set_db_path(self, db_path):
        self._db_path = db_path

    def set_db_name(self, db_name):
        self._db_name = db_name

    def _setup(self):
        """
        Setup the FileDataBase class with pre-settings
        :return:
        """
        if self._db_path is None:
            self._db_path = os.path.join(os.path.expanduser("~"), "STA")
        elif os.path.expanduser("~") not in self._db_path:
            self._db_path = os.path.join(os.path.expanduser("~"), self._db_path)

        if self._db_name is None:
            self._db_name = "db0"

        #create the individual database names from the names
        self._db_user_name = "{0}_users.csv".format(self._db_name)
        self._db_tracks_name = "{0}_tracks.csv".format(self._db_name)

    def create_db_user(self):
        self._setup()

        print("DBFile:CreateDbUser")

        #create folder which contains the database if not existing:
        if os.path.exists(self._db_path) is False:
            os.mkdir(self._db_path)
            print("Data location successfully created")
            print(" - ", self._db_path)
        else:
            print("Data location exists already")
            print(" - ", self._db_path)


        if os.path.exists(os.path.join(self._db_path, self._db_user_name)) is False:
            f = open(os.path.join(self._db_path, self._db_user_name), "w")
            f.write("|#- SportsTrackerAnalyzer User Database")
            f.close()
            print("SportsTrackerAnalyzer User Database created under:")
            print(" - ", os.path.join(self._db_path, self._db_user_name))
        else:
            print("SportsTrackerAnalyzer User Database exists already under:")
            print(" - ", os.path.join(self._db_path, self._db_user_name))

    def create_db_tracks(self):
        self._setup()

        print("DBFile:CreateDbTracks")

        #create folder which contains the database if not existing:
        if os.path.exists(self._db_path) is False:
            os.mkdir(self._db_path)
            print("Data location successfully created")
            print(" - ", self._db_path)
        else:
            print("Data location exists already")
            print(" - ", self._db_path)

        if os.path.exists(os.path.join(self._db_path, self._db_tracks_name)) is False:
            f = open(os.path.join(self._db_path, self._db_tracks_name), "w")
            f.write("|#- SportsTrackerAnalyzer Tracks Database")
            f.close()
            print("SportsTrackerAnalyzer Tracks Database created under:")
            print(" - ", os.path.join(self._db_path, self._db_tracks_name))
        else:
            print("SportsTrackerAnalyzer Tracks Database exists already under:")
            print(" - ", os.path.join(self._db_path, self._db_tracks_name))

    def test_db_user(self):
        self._setup()

        exists = False
        if os.path.join(self._db_path, self._db_user_name):
            #another validity check (?)
            exists = True

        return exists

    def test_db_tracks(self):
        self._setup()

        exists = False
        if os.path.join(self._db_path, self._db_tracks_name):
            # another validity check (?)
            exists = True

        return exists

    def create_user(self, init_user_dictionary=None):
        self._setup()

        hash_str = "{surname}{lastname}{birthday}".format(surname=init_user_dictionary.get("user_surname"),
                                                          lastname=init_user_dictionary.get("user_lastname"),
                                                          birthday=init_user_dictionary.get("user_birthday"))
        md5_hash = hashlib.md5(hash_str.encode("utf-8")).hexdigest()[0:8]
        uuid_hash = str(uuid.uuid4()).split("-")[0]
        init_user_dictionary['user_hash'] = f"{md5_hash}{uuid_hash}"

        f = open(os.path.join(self._db_path, self._db_user_name), "a")
        f.write(json.dumps(init_user_dictionary)+"\n")
        f.close()

    def search_user(self, pairs=None):
        self._setup()

        if isinstance(pairs, dict):
            pairs = [pairs]

        f = open(os.path.join(self._db_path, self._db_user_name), "r")

        f_ids = []
        for i_user in f:
            #ignore comments:
            if i_user.find("|#-") == 0:
                continue
            if len(i_user) == 0:
                continue

            i_obj = json.loads(i_user)

            for i_search in pairs:
                i_key = list(i_search.keys())[0]
                i_val = list(i_search.values())[0]

                if i_obj.get(i_key) != i_val:
                    #We skip the individual search pair of key/value if not existing in i_obj
                    continue

                if i_obj.get("user_hash") not in f_ids:
                    #if key/value exists we add the hash
                    f_ids.append(i_obj.get("user_hash"))

        f.close()

        return f_ids

    def search_user_by_hash(self, hash=None):
        self._setup()
        f = open(os.path.join(self._db_path, self._db_user_name), "r")
        ret = None
        for i_user in f:
            i_obj = json.loads(i_user)
            if i_obj.get("user_hash") == hash:
                ret = i_obj
                break
        f.close()
        return ret

    def mod_user_by_hash(self, hash, key, value, date):
        """
        Modify the user database
        :param key:
        :param value:
        :return:
        """
        self._setup()
        f = open(os.path.join(self._db_path, self._db_user_name), "r")
        ret = []
        for i_entry in f:
            i_obj = json.loads(i_entry)
            if i_obj.get("user_hash") != hash:
                ret.append(i_obj)
                continue
            i_obj[key] = value
            ret.append(i_obj)
        f.close()

        f = open(os.path.join(self._db_path, self._db_user_name), "w")
        for i_entry in ret:
            f.write(json.dumps(i_entry)+"\n")

        f.close()
        return ret