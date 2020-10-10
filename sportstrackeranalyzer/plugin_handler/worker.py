import argparse

from sportstrackeranalyzer.plugin_handler.loader import PluginLoader
from sportstrackeranalyzer.module.db_handler import DataBaseHandler

#Add a argparser to make life simpler for now:
parser = argparse.ArgumentParser()
#parser.add_argument('_', nargs='*')
parser.add_argument('--route-by-hash', dest='route_by_hash', type=str, default=None)
args = parser.parse_args()

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

overwrite = False

pl = PluginLoader()
pl.set_database_handler(dbh=dbh)

all_available_plugins = pl.get_all_plugins()




for i_track in user_tracks:

    # print()
    i_track_hash = i_track.get("track_hash")

    if args.route_by_hash is not None and args.route_by_hash != i_track_hash:
        continue

    print(i_track)

    existing_leaves = dbh.get_all_leaves_for_track(track_hash=i_track_hash)
    if existing_leaves is None:
        #if existing_leaves is none, there are no leaves in this track
        continue

    existing_leaf_names = list(existing_leaves.keys())


    print("Existing leaves:", existing_leaf_names, i_track_hash)

    pl.set_existing_leaves_for_track(existing_leaves=existing_leaves)
    pl.set_track_by_hash(track_hash=i_track_hash)
    pl.allow_overwrite()

    for i_plugin in all_available_plugins:
        # error codes:
        # 2: leaf exits but no overwriting is allowed
        # 1: leaf can not be processed due to missing processed leaves or raw data
        # 0: OK
        # -1: Something went wrong
        error_code = pl.process(i_plugin)