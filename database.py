from sqlite3 import threadsafety
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm import declarative_base

Base = declarative_base()
engine = create_engine("sqlite:///./memory.db", echo=True)
session = sessionmaker(bind=engine, autocommit=False, autoflush=False, threadsafety = False)


def get_db():
    ses = Session(engine)
    return ses