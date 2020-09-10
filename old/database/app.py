import os

from sqlalchemy import or_

from constants import *
from database.schema import Citizen, purge_data, setup_database, session
from database.setup import create_citizens


def init_database(args):
    if args.new_database:
        print('Building new database from scratch..')
        purge_data()
    elif os.path.isfile(DATABASE_PATH):
        print('Database found')
        return
    else:
        print('Database not found. Building new from scratch..')
    setup_database()
    create_citizens()
    print('Database is ready to use')


def search_person_any(search_string):
    search_string = search_string.capitalize()
    return (
        session.query(Citizen)
        .filter(or_(
            Citizen.first_name == search_string,
            Citizen.last_name == search_string,
            Citizen.citizen_id == search_string,
        ))
        .order_by(Citizen.last_name)
    )


def search_person_full_name(first_name, last_name):
    first_name = first_name.capitalize()
    last_name = last_name.capitalize()
    return (
        session.query(Citizen)
        .filter(
            Citizen.first_name == first_name,
            Citizen.last_name == last_name,
        )
        .order_by(Citizen.last_name)
    )

