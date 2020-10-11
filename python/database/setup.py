import contextlib

from database.schema import Base, Citizen, citizen_database, engine
from database.helper import (
    CitizenIDGenerator,
    fake,
    gender_id_to_name,
    generate_name,
    named_citizens,
    SectorGenerator,
)

NUM_RANDOM_CITIZENS = 20_000
CHUNK_SIZE = 10_000
NUM_CHUNKS = int(NUM_RANDOM_CITIZENS / CHUNK_SIZE)

sectors = SectorGenerator()


def create_named_citizens():
    for citizen in named_citizens:
        citizen_database.session.add(Citizen(**citizen))


def create_random_citizens():
    print(f'Creating {NUM_RANDOM_CITIZENS} random citizens...')
    for i in range(NUM_CHUNKS):
        print(f'Progress: {(i / NUM_CHUNKS) * 100}% complete', end='\r')
        citizen_database.session.bulk_insert_mappings(
            Citizen,
            [
                create_citizen(CitizenIDGenerator())
                for _ in range(CHUNK_SIZE)
            ]
        )
    print(f'Created {NUM_RANDOM_CITIZENS} random citizens')


def create_citizen(id_generator):
    citizen_id = next(id_generator)
    gender = int(citizen_id[-1])
    first_name, last_name = generate_name(gender)
    return {
        'citizen_id': citizen_id,
        'first_name': first_name,
        'last_name': last_name,
        'gender': gender,
        'gender_name': gender_id_to_name[gender],
        'birthdate': fake.date_of_birth(),
        'sector': sectors.random(),
    }


def truncate_database():
    with contextlib.closing(engine.connect()) as con:
        trans = con.begin()
        con.execute(
            'TRUNCATE {} RESTART IDENTITY;'.format(
                ','.join(
                    table.name for table in reversed(
                        Base.metadata.sorted_tables
                    )
                )
            )
        )
        trans.commit()


def create_citizens():
    with citizen_database:
        create_named_citizens()
        create_random_citizens()
        citizen_database.session.commit()


if __name__ == '__main__':
    truncate_database()
    create_citizens()
