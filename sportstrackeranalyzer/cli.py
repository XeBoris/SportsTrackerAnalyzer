"""Console script for sportstrackeranalyzer."""
import argparse
import sys
import os
import datetime
import shelve

from .module.db_handler import DataBaseHandler

from .module.simple_actions import create_db
from .module.simple_actions import load_db
from .module.simple_actions import add_user
from .module.simple_actions import set_user
from .module.simple_actions import mod_user
from .module.simple_actions import list_user
from .module.simple_actions import find_tracks
from .module.simple_actions import remove_tracks
from .module.simple_actions import remove_leaves
from .module.simple_actions import collect_cli_user_info
from .module.simple_actions import add_tracks



shelve_temp = os.path.join(os.path.expanduser("~"), ".sta")

def main():
    """Console script for sportstrackeranalyzer."""
    parser = argparse.ArgumentParser()
    parser.add_argument('_', nargs='*')
    parser.add_argument('--type', dest='type', type=str)
    parser.add_argument('--path', dest='path', type=str)

    parser.add_argument('--key', dest='key', type=str)
    parser.add_argument('--value', dest='value', type=str)
    parser.add_argument('--date', dest='date', type=str)
    parser.add_argument('--hash', dest='hash', type=str)
    parser.add_argument('--overwrite', dest='overwrite', action='store_true')


    parser.add_argument('--track-source', dest='track_source', type=str) #runtastic, strava,...
    parser.add_argument('--source-type', dest='source_type', type=str) #db-dump, gps, online

    args = parser.parse_args()

    print("Arguments: " + str(args))
    print("Replace this message by putting your code into "
          "sportstrackeranalyzer.cli.main")

    print(args._)

    if args._[0] == "createDB":
        db_name = args._[1]
        db_path = args.path
        db_type = args.type
        create_db(db_type=db_type,
                  db_path=db_path,
                  db_name=db_name)
    elif args._[0] == "loadDB":
        db_name = args._[1]
        db_path = args.path
        db_type = args.type
        load_db(db_type=db_type,
                db_path=db_path,
                db_name=db_name)

    elif args._[0] == "setUser":
        db_user = args._[1]
        set_user(db_user=db_user)

    elif args._[0] == "addUser":
        init_user_dictionary = collect_cli_user_info()
        add_user(init_user_dictionary)

    elif args._[0] == "listUser":
        list_user()

    elif args._[0] == "modUser":
        #prepare to modify the user database
        db_key = args.key
        db_value = args.value
        db_date = args.date
        mod_user(key=db_key,
                 value=db_value,
                 date=db_date)

    elif args._[0] == "addTracks":
        track_source = args.track_source
        source_type = args.source_type
        overwrite = args.overwrite
        input_path = args.path
        date_obj = args.date

        add_tracks(track_source=track_source,
                   source_type=source_type,
                   input_path=input_path,
                   overwrite=overwrite,
                   date_obj=date_obj)



    elif args._[0] == "findTracks":
        track_source = args.track_source
        source_type = args.source_type
        date = args.date

        find_tracks(track_source, source_type, date)

    elif args._[0] == "removeTracks":
        track_hash = args.hash

        remove_tracks(track_hash)

    elif args._[0] == "removeLeaves":
        track_hash = args.hash

        remove_leaves(track_hash)

    elif args._[0] == "authorizeStrava":
        from .module.strava_auth_routes import urls_blueprint
        import webbrowser
        from threading import Timer
        from flask import Flask

        def open_browser():
            webbrowser.open_new('http://127.0.0.1:5000/')


        app = Flask(__name__)
        app.register_blueprint(urls_blueprint)
        Timer(1, open_browser).start()
        app.run(debug=True)


    return 0




if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
