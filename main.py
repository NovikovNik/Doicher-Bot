from lib2to3.pytree import Base
from models import *
from database import *
from bot import start_pooling


if __name__ == "__main__":
    if debug:=False == True:
        Base.metadata.drop_all(engine) ##Убрать позже
    Base.metadata.create_all(engine)
    database = get_db()
    start_pooling()
    