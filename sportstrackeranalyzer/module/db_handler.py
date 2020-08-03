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

    def search_user(self, pairs=None):
        return self._handler_type.search_user(pairs)

    def search_user_by_hash(self, hash=None):
        return self._handler_type.search_user_by_hash(hash=hash)

    def create_db_tracks(self):
        return self._handler_type.create_db_tracks()

    def test_db_user(self):
        return self._handler_type.test_db_user()

    def test_db_tracks(self):
        return self._handler_type.test_db_tracks()