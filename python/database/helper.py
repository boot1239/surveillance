import math
import random

from faker import Faker

fake = Faker('en_US')

GENDER_WEIGHTS = (45, 45, 10)

SECTORS = ('A', 'B', 'C', 'D')
SECTOR_WEIGHTS = (45, 15, 40, 5)

MIN_CITIZEN_ID_PREFIX = 10_000
MAX_CITIZEN_ID_PREFIX = 99_999
MIN_CITIZEN_ID_SUFFIX = 100
MAX_CITIZEN_ID_SUFFIX = 999

CITIZEN_ID_FORMAT = '{prefix}-{middle}-{suffix}{gender}'

named_citizens = [
    {
        'first_name': 'Max',
        'last_name': 'Rodney',
        'citizen_id': '32768-3298',
        'gender': 1,
        'gender_name': 'male',
        'birthdate': '1972-04-24',
        'sector': 'A'
    },
]
named_citizen_ids = [citizen['citizen_id'] for citizen in named_citizens]

gender_id_to_name = {
    0: 'male',
    1: 'female',
    2: 'non-binary',
}


class SectorGenerator:
    def __init__(self, sectors=SECTORS, sector_weights=SECTOR_WEIGHTS):
        self.weighted_sectors = []
        for i, weight in enumerate(sector_weights):
            self.weighted_sectors.extend(sectors[i] * weight)

    def random(self):
        return random.choice(self.weighted_sectors)


def generate_name(gender):
    if gender == 0:
        name = (fake.first_name_male(), fake.last_name_male())
    elif gender == 1:
        name = (fake.first_name_female(), fake.last_name_female())
    else:
        name = (fake.first_name_nonbinary(), fake.last_name_nonbinary())

    return name


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


class CitizenIDGenerator:
    def __init__(self):
        self.prefix_ids = random_range(
            MIN_CITIZEN_ID_PREFIX,
            MAX_CITIZEN_ID_PREFIX,
        )
        self.suffix_ids = random_range(
            MIN_CITIZEN_ID_SUFFIX,
            MAX_CITIZEN_ID_SUFFIX,
        )
        self.gender = GenderGenerator()

    def __iter__(self):
        return self

    def __next__(self):
        return CITIZEN_ID_FORMAT.format(
            prefix=next(self.prefix_ids),
            middle=next(self.suffix_ids),
            suffix=next(self.suffix_ids),
            gender=self.gender.random(),
        )


class GenderGenerator:
    # Male: 0, Female: 1, Non-binary: 2

    def __init__(self, weights=GENDER_WEIGHTS):
        self.genders = []
        for i, weight in enumerate(weights):
            self.genders.extend([i] * weight)

    def random(self):
        return random.choice(self.genders)
