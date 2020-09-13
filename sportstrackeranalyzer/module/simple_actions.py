import sys
import os
import datetime
import shelve

from .db_handler import DataBaseHandler
from .shelve_handler import ShelveHandler

"""
This file contains simple actions which are defined outside of classes because of their simplicity
"""


def create_db(db_type=None,
              db_name=None,
              db_path=None):

    dbh = DataBaseHandler(db_type=db_type)
    dbh.set_db_path(db_path=db_path)
    dbh.set_db_name(db_name=db_name)

    dbh.create_db_user()
    dbh.create_db_tracks()

def load_db(db_type=None,
            db_name=None,
            db_path=None):

    dbh = DataBaseHandler(db_type=db_type)
    dbh.set_db_path(db_path=db_path)
    dbh.set_db_name(db_name=db_name)

    db_file_exists = dbh.get_database_exists()
    db_tables_exists = dbh.get_database_tables_exists()

    if db_file_exists is True and db_tables_exists is True:
        db = {'db_name': db_name, 'db_type': db_type, 'db_path': db_path}

        db_temp = ShelveHandler()
        db_temp.write_shelve(db)


def collect_cli_user_info():
    user_surname = input("Surname: ")
    user_lastname = input("Lastname: ")
    user_username = input("Username: ")
    user_birthday = input("Birthday: ")
    user_weight = input("Weight: ")
    user_height = input("Height: ")
    user_sex = input("Sex: ")

    retdict = {"user_surname": user_surname,
               "user_lastname": user_lastname,
               "user_username": user_username,
               "user_birthday": user_birthday,
               "user_weight": [{str(datetime.datetime.now().timestamp()): user_weight}],
               "user_height": user_height,
               "user_sex": user_sex}
    return retdict

def set_user(db_user=None):
    """
    This function allows to overwrite/set a pre-defined user to which new records/tracks
    are added.
    :param db_user:
    :return:
    """

    db_temp = ShelveHandler()
    db_dict = db_temp.read_shelve_by_keys(["db_name", "db_type", "db_path"])

    dbh = DataBaseHandler(db_type=db_dict["db_type"])
    dbh.set_db_path(db_path=db_dict["db_path"])
    dbh.set_db_name(db_name=db_dict["db_name"])

    #test if requested user is part of the database
    search_result = dbh.search_user(db_user, by="username")
    nb_search_result = len(search_result)

    if len(search_result) == 1:
        #Update Shelve:
        db = {"db_user": search_result[0].get("user_username"),
              "db_hash": search_result[0].get("user_hash")}

        db_temp.write_shelve(db)
        print(f"Assume to add tracks for user: {db_user}")
    elif len(search_result) == 0:
        print(f"Username {db_user} is not found in current user database.")
        print("Add user first...")
    else:
        print("We have found multiple user ids. Please select the one you are referring to:")
        for k, db_entry in enumerate(search_result):

            p = "[{k}] | Name: {user_surname} {user_lastname} | Username: {user_username}".format(k=k,
                                                                                              user_surname=db_entry.get("user_surname"),
                                                                                              user_lastname=db_entry.get("user_lastname"),
                                                                                              user_username=db_entry.get("user_username")
                                                                                              )
            print(p)
        print("Choose a number:")
        selected_hash = input(f"Select number 0 to {nb_search_result-1}: ")
        selected_hash = search_result[int(selected_hash)]

        #Update Shelve:
        db = {"db_user": selected_hash.get("user_username"),
              "db_hash": selected_hash.get("user_hash")}

        db_temp.write_shelve(db)

    del db_temp

def add_user(init_user_dictionary):

    db_temp = ShelveHandler()
    db_dict = db_temp.read_shelve_by_keys(["db_name", "db_type", "db_path"])

    dbh = DataBaseHandler(db_type=db_dict["db_type"])
    dbh.set_db_path(db_path=db_dict["db_path"])
    dbh.set_db_name(db_name=db_dict["db_name"])

    dbh.create_user(init_user_dictionary)

    del db_temp

def mod_user(key, value, date):

    db_temp = ShelveHandler()
    db_dict = db_temp.read_shelve_by_keys(["db_name",
                                           "db_type",
                                           "db_path",
                                           "db_user",
                                           "db_hash"])

    dbh = DataBaseHandler(db_type=db_dict["db_type"])
    dbh.set_db_path(db_path=db_dict["db_path"])
    dbh.set_db_name(db_name=db_dict["db_name"])

    dbh.mod_user_by_hash(db_dict["db_hash"], key, value, date)