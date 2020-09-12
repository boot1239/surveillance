import contextlib
import math
import random

from faker import Faker

from database.schema import Base, Citizen, citizen_database, engine

NUM_RANDOM_CITIZENS = 20_000
CHUNK_SIZE = 10_000
NUM_CHUNKS = int(NUM_RANDOM_CITIZENS / CHUNK_SIZE)
MIN_PERSON_ID = 10_000_000
MAX_PERSON_ID = 99_999_999

fake = Faker()

named_citizens = [
    {
        'first_name': 'Max',
        'last_name': 'Rodney',
        'citizen_id': 29582203,
        'gender': 'M',
        'birthdate': '1972-04-24',
        'address': 'Not known',
        'current_location': 'Not known',
    },
]
named_citizen_ids = [citizen['citizen_id'] for citizen in named_citizens]


def create_named_citizens():
    for citizen in named_citizens:
        citizen_database.session.add(Citizen(**citizen))


def create_random_citizens():
    citizen_ids = random_range(MIN_PERSON_ID, MAX_PERSON_ID)
    citizen_id_generator = (
        str(x) for x in citizen_ids if x not in named_citizen_ids
    )
    print(f'Creating {NUM_RANDOM_CITIZENS} random citizens...')
    for i in range(NUM_CHUNKS):
        print(f'Progress: {(i / NUM_CHUNKS) * 100}% complete', end='\r')
        citizen_database.session.bulk_insert_mappings(
            Citizen,
            [
                create_citizen(citizen_id_generator)
                for _ in range(CHUNK_SIZE)
            ]
        )
    print(f'Created {NUM_RANDOM_CITIZENS} random citizens')


def create_citizen(id_generator):
    profile = fake.profile()
    name = profile['name'].split(' ')
    return {
        'citizen_id': next(id_generator),
        'first_name': name[0],
        'last_name': name[1],
        'gender': profile['sex'],
        'birthdate': profile['birthdate'],
        'address': profile['address'],
        'current_location': fake.local_latlng(),
    }


def random_range(start, stop=None, step=None):
    if stop is None:
        start, stop = 0, start
    if step is None:
        step = 1

    def mapping(i):
        return (i * step) + start

    maximum = (stop - start) // step
    value = random.randint(0, maximum)
    offset = random.randint(0, maximum) * 2 + 1
    multiplier = 4 * (maximum // 4) + 1
    modulus = int(2 ** math.ceil(math.log2(maximum)))
    found = 0
    while found < maximum:
        if value < maximum:
            found += 1
            yield mapping(value)

        value = (value * multiplier + offset) % modulus


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
