from word_generator import get_words_from_list
from lib2to3.pytree import Base
from models import *
from database import *

if __name__ == "__main__":
    if debug:=True == True:
        Base.metadata.drop_all(engine) ##Убрать позже
    Base.metadata.create_all(engine)
    database = get_db()
    
    get_words_from_list('German.txt')
    