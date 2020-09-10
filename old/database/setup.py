import random

from constants import *
from database.schema import Citizen, session
from helpers import print_progress_bar, random_range


def create_named_citizens():
    villain = Citizen(
        first_name=VILLAIN_FIRST_NAME,
        last_name=VILLAIN_LAST_NAME,
        citizen_id=VILLAIN_PERSON_ID,
    )
    session.add(villain)


def create_random_citizens():
    print('Making list of random citizen ids..')
    citizen_ids = random_range(MIN_PERSON_ID, MAX_PERSON_ID)
    citizen_id_generator = (
        str(x) for x in citizen_ids if x not in NAMED_CITIZENS_IDS
    )

    print('Making list of random names..')
    with open('database/first_names.txt') as file:
        first_names = [line.rstrip('\n') for line in file]
    with open('database/last_names.txt') as file:
        last_names = [line.rstrip('\n') for line in file]
    names = (
        (random.choice(first_names), random.choice(last_names))
        for _ in range(NUM_RANDOM_CITIZENS)
    )

    print('Creating entries in database from lists..')
    print_progress_bar(0, NUM_RANDOM_CITIZENS)
    for i, chunk in enumerate(zip(*[names] * CHUNK_SIZE)):
        session.bulk_insert_mappings(
            Citizen,
            [
                {
                    'first_name': first_name,
                    'last_name': last_name,
                    'citizen_id': next(citizen_id_generator),
                }
                for j, (first_name, last_name) in enumerate(chunk)
            ]
        )
        print_progress_bar(i + 1, NUM_RANDOM_CITIZENS / CHUNK_SIZE)
    print('Entries created')


def create_citizens():
    print('Creating citizens..')
    create_named_citizens()
    create_random_citizens()
    print('Committing to database..')
    session.commit()
