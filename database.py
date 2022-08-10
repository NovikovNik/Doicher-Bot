from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm import declarative_base

Base = declarative_base()
engine = create_engine("sqlite:///./memory.db", echo=True)
session = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db():
    ses = session
    return ses