from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from constants import *

Base = declarative_base()
engine = create_engine(f'sqlite:///{DATABASE_PATH}')
db_session = sessionmaker(bind=engine)
session = db_session()


class Citizen(Base):
    __tablename__ = 'citizen'
    id = Column('id', Integer, primary_key=True)
    first_name = Column('first_name', String, nullable=False)
    last_name = Column('last_name', String, nullable=False)
    citizen_id = Column('citizen_id', String, nullable=False, unique=True)

    UniqueConstraint('first_name', 'last_name')


def setup_database():
    Base.metadata.create_all(engine)
    print('Database built')


def purge_data():
    session.query(Citizen).delete()
    session.commit()
