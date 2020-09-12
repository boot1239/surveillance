from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DATABASE_PW = 'x2tMPrXYPCiR5g9dp9Dd27qRnL4aXk'
DATABASE_URL = f'postgresql://nss:{DATABASE_PW}@localhost/citizen'

Base = declarative_base()
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
session_maker = sessionmaker(bind=engine)


class database_handler:
    def __enter__(self):
        self.session = session_maker()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()


citizen_database = database_handler()


class Citizen(Base):
    __tablename__ = 'citizen'
    id = Column('id', Integer, primary_key=True)
    citizen_id = Column('citizen_id', Integer, nullable=False, unique=True)
    first_name = Column('first_name', String, nullable=False)
    last_name = Column('last_name', String, nullable=False)
    gender = Column('gender', String, nullable=False)
    birthdate = Column('birthdate', String, nullable=False)
    address = Column('address', String, nullable=False)
    current_location = Column('current_location', String, nullable=False)

    UniqueConstraint('first_name', 'last_name')



