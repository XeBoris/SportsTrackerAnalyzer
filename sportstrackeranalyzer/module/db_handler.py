from .db_files import FileDataBase

class DataBaseHandler(FileDataBase):
    def __init__(self, db_type=None):
        self._db_type = db_type
        self._handler_type = None

        if self._db_type == "FileDataBase":
            self._handler_type = FileDataBase()
        else:
            self._handler_test()


    def _handler_test(self):
        if self._handler_type is None:
            print("You need to specify a database backend handler")
            print("Choose:")
            print(" - FileDataBase")
            exit()

    def set_db_path(self, db_path=None):
        self._handler_type.set_db_path(db_path=db_path)

    def set_db_name(self, db_name=None):
        self._handler_type.set_db_name(db_name=db_name)

    def create_db_user(self):
        return self._handler_type.create_db_user()

    def create_user(self, init_user_dictionary=None):
        return self._handler_type.create_user(init_user_dictionary)

    def mod_user_by_hash(self, hash, key, value, date):
        return self._handler_type.mod_user_by_hash(hash, key, value, date)

    def search_user(self, user=None, by=None):
        return self._handler_type.search_user(user, by)

    def search_user_by_hash(self, hash=None):
        return self._handler_type.search_user_by_hash(hash=hash)

    def create_db_tracks(self):
        return self._handler_type.create_db_tracks()

    def test_db_user(self):
        return self._handler_type.test_db_user()

    def test_db_tracks(self):
        return self._handler_type.test_db_tracks()

    #This part handles write/read operations on the tracks database:
    #  - Tracks are like branches of a tree
    def write_branch(self, db_operation="new", track=None, track_hash=None):
        return self._handler_type.write_branch(db_operation, track, track_hash)

    def read_branch(self, key=None, attribute=None):
        return self._handler_type.read_branch(key=key, attribute=attribute)

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
        return self._handler_type.write_leaf(directory=directory,
                                             track_hash=track_hash,
                                             leaf_hash=leaf_hash,
                                             leaf_config=leaf_config,
                                             leaf=leaf,
                                             leaf_type=leaf_type)

    def read_leaf(self):
        return self._handler_type.read_leaf()


    # Gets:
    def get_database_exists(self):
        return self._handler_type.get_database_exists()

    def get_database_tables_exists(self):
        return self._handler_type.get_database_tables_exists()

