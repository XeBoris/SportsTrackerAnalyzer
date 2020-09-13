import os
import uuid
import json
import hashlib
from tinydb import TinyDB, Query

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
        self._db_name_final = f"db-{self._db_name}.tiny"
        self._db_table_users = f"db_{self._db_name}_users"
        self._db_table_tracks = f"db_{self._db_name}_branches"

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

        if self._test_db_table_exists(self._db_table_users) is False:
            db = TinyDB(os.path.join(self._db_path, self._db_name_final))
            tb = db.table(self._db_table_users)
            tb.insert({"init": {"version": 1, "table": self._db_table_users}})
            db.close()
            print(f"TinyDB database {self._db_name_final} created wit table {self._db_table_users}")
        else:
            print(f"TinyDB table {self._db_table_users} exists already")

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

        if self._test_db_table_exists(self._db_table_tracks) is False:
            db = TinyDB(os.path.join(self._db_path, self._db_name_final))
            tb = db.table(self._db_table_tracks)
            tb.insert({"init": {"version": 1, "table": self._db_table_tracks}})
            db.close()
            print(f"TinyDB database {self._db_name_final} created wit table {self._db_table_tracks}")
        else:
            print(f"TinyDB table {self._db_table_tracks} exists already")

    def _test_db_exists(self):
        """
        Private member function
        :return:
        """
        exists = False
        if os.path.exists(os.path.join(self._db_path, self._db_name_final)):
            exists = True
        return exists

    def _test_db_table_exists(self, tablename):
        """
        private member function
        :param tablename:
        :return:
        """
        exists = False
        if self._test_db_exists():
            db = TinyDB(os.path.join(self._db_path, self._db_name_final))
            all_tables = db.tables()
            if tablename in all_tables:
                exists = True
        return exists

    def get_database_exists(self):
        self._setup()
        return self._test_db_exists()

    def get_database_tables_exists(self):
        """
        Check if all required tables are created during initial creation process
        :return:
        """
        self._setup()

        no_missing_table = True
        for i_table in [self._db_table_users, self._db_table_tracks]:
            table_exists = self._test_db_table_exists(i_table)
            if table_exists is False:
                no_missing_table = False
                break
        return no_missing_table

    def create_user(self, init_user_dictionary=None):
        self._setup()

        hash_str = "{surname}{lastname}{birthday}".format(surname=init_user_dictionary.get("user_surname"),
                                                          lastname=init_user_dictionary.get("user_lastname"),
                                                          birthday=init_user_dictionary.get("user_birthday"))
        md5_hash = hashlib.md5(hash_str.encode("utf-8")).hexdigest()[0:8]
        uuid_hash = str(uuid.uuid4()).split("-")[0]
        init_user_dictionary['user_hash'] = f"{md5_hash}{uuid_hash}"

        #ToDO Write some exceptions:
        db = TinyDB(os.path.join(self._db_path, self._db_name_final))
        db.default_table_name = self._db_table_users
        db.insert(init_user_dictionary)
        db.close()


    def search_user(self, user, by="username"):
        self._setup()

        #ToDO Write some exceptions:
        db = TinyDB(os.path.join(self._db_path, self._db_name_final))
        db.default_table_name = self._db_table_users

        User = Query()
        p = []
        if by == "username":
            p = db.search(User.user_username == user)
        elif by == "surname":
            p = db.search(User.user_surname == user)
        elif by == "lastname":
            p = db.search(User.user_lastname == user)
        elif by == "hash":
            p = db.search(User.user_hash == user)

        db.close()
        return p

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

     #This part handles write/read operations on the tracks database:
    #  - Tracks are like branches of a tree
    def _open_tiny_db(self):
        self._setup()
        self.db = TinyDB(os.path.join(self._db_path, self._db_name_final))
        self.db.default_table_name = self._db_table_tracks  # <- tracks are branches!
        self.user = Query()

    def _close_tiny_db(self):
        self.db.close()



    def write_branch(self,
                     db_operation="new",
                     track=None,
                     track_hash=None
                     ):
        """
        A track has is a branch. And each branch will have leaves!
        To write a branch/track with write_branch(..) you can create a "new" branch or
        "update" an existing branch with this function.
        :param db_operation:
        :param track:
        :return:
        """
        self._open_tiny_db()
        print("sss")
        if db_operation == "new" and track_hash is not None and track is not None:
            find_hash = self.db.get(self.user["track_hash"] == track_hash)
            if find_hash is None:
                self.db.insert(track)
            else:
                print("No new entry possible")
        elif db_operation == "update" and track_hash is not None and track is not None:
            #identify first
            find_hash = self.db.get(self.user["track_hash"] == track_hash)
            if find_hash is None:
                # This if conditions behavies like the "new" option
                self.db.insert(track)
            elif find_hash is not None:
                # Update dictionary with new track information:
                find_hash.update(track)
                # Get hash ID from database for update procedure
                find_hash_id = find_hash.doc_id
                # Update a branch if existing!
                self.db.update(find_hash, doc_ids=[find_hash_id])
            else:
                print("do something else")

        else:
            print("You are trying to handling an unknown database operation!")
        self._close_tiny_db()

    def read_branch(self, key=None, attribute=None):
        self._open_tiny_db()
        db_entry = self.db.search(self.user[key] == attribute)
        self._close_tiny_db()
        return db_entry

    #This part handles write/read operation on metadata
    #  - metadata to tracks are like leaves which belong to branch

    def write_leaf(self,
                   directory=None,
                   track_hash=None,
                   leaf_hash=None,
                   leaf_config=None,
                   leaf=None,
                   leaf_type=None
                   ):
        """
        Writing a leaf consist of two operations:
        1) Write the leaf
        2) Adjust the track/branch record
        :param directory:
        :param track_hash:
        :param leaf_hash:
        :param leaf_config:
        :param leaf:
        :param leaf_type:
        :return:
        """

        if os.path.exists(os.path.join(directory)) is False:
            os.makedirs(directory)

        self._open_tiny_db()

        # Get the according branch/track from the tinyDB
        find_hash = self.db.get(self.user["track_hash"] == track_hash)
        if find_hash is None:
            return False
        find_hash_id = find_hash.doc_id

        # We start to write/update according to the chosen method:
        if leaf_type == "DataFrame":
            # Write the leaf to disk:
            leaf.to_csv(path_or_buf=os.path.join(directory, f"{leaf_hash}.csv"),
                        index=False,
                        #compression="gzip",
                        )

            # Update the leaf in the track database
            if 'leaf' not in find_hash:
                db_entry = {}
            else:
                db_entry = find_hash.get("leaf")

            db_entry[leaf_config['name']] = leaf_config
            self.db.update({'leaf': db_entry}, doc_ids=[find_hash_id])

        # find_hash = self.db.get(self.user["track_hash"] == track_hash)
        # print(find_hash)

        self._close_tiny_db()
        return True

    def read_leaf(self):
        self._open_tiny_db()

        self._close_tiny_db()
