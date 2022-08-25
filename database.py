from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

Base = declarative_base()
engine = create_engine("sqlite:///./database/memory.db", echo=False)
session = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db():
    ses = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    return ses
