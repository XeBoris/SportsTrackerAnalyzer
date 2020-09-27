from sportstrackeranalyzer.plugin_handler.loader import PluginLoader
from sportstrackeranalyzer.module.db_handler import DataBaseHandler

db_type = "FileDataBase"
db_path = "/home/koenig/STAtest"
db_name = "testDB"

dbh = DataBaseHandler(db_type=db_type)
dbh.set_db_path(db_path=db_path)
dbh.set_db_name(db_name=db_name)

db_exists = dbh.get_database_exists()
if db_exists is False:
    print(f"Database {db_name} does not exists")
    exit()
else:
    print(f"Database {db_name} does exists")

user_name = "koenig"

user_entry = dbh.search_user(user=user_name, by="username")

user_hash = user_entry[0].get("user_hash")
print(user_name, user_hash)

user_tracks = dbh.read_branch(key="user_hash", attribute=user_hash)


pl = PluginLoader()
pl.set_database_handler(dbh=dbh)

all_available_plugins = pl.get_all_plugins()


for i_track in user_tracks:
    # print(i_track)
    # print()
    i_track_hash = i_track.get("track_hash")

    existing_leaves = dbh.get_all_leaves_for_track(track_hash=i_track_hash)
    if existing_leaves is None:
        #if existing_leaves is none, there are no leaves in this track
        continue

    existing_leaf_names = list(existing_leaves.keys())


    print("Existing leaves:", existing_leaf_names, i_track_hash)

    pl.set_existing_leaves_for_track(existing_leaves=existing_leaves)
    pl.set_track_by_hash(track_hash=i_track_hash)

    for i_plugin in all_available_plugins:
        pl.process(i_plugin)