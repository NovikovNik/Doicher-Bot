from lib2to3.pytree import Base
from database import *
from bot_body import start_pooling


if __name__ == "__main__":
    if debug := True == True:
        Base.metadata.drop_all(engine)  # Убрать позже
    Base.metadata.create_all(engine)
    database = get_db()
    start_pooling()
