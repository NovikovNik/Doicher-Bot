from datetime import datetime
import pytz
from database import get_db
import models

db = get_db()


def initial_user_create(user_name: str, nick: str, chat_id: id) -> None:
    with db.begin():
        new_user = models.User(name=user_name,
                               first_authorization=datetime.now(),
                               nick_name=nick,
                               chat_id=chat_id)
        add_user(new_user)


def add_user(user):
    with db.begin() as session:
        session.add(user)
        session.commit()
        # session.refresh(user)


def find_user_in_db(user_id: int) -> models.User:
    with db.begin() as session:
        user = session.query(models.User).filter(
            models.User.name == user_id).first()
        return user


def delete_user_from_db(user_id: int) -> None:
    with db.begin() as session:
        session.query(models.User).filter(models.User.name == user_id).delete()
        session.commit()


def add_new_word_to_db(chat_id: int, word: str) -> None:
    with db.begin() as session:
        name = session.query(models.User.name).filter(
            models.User.chat_id == chat_id).first()
        new_word = models.Words(
            user_id=name[0], word=word, time_stamp=datetime.now())
        session.add(new_word)
        session.commit()
        # session.refresh(new_word)


def create_word_object(chat_id, word):
    return models.Words(user_id = chat_id, word = word, time_stamp=datetime.now())
        
        
def bulk_insert_new_words_to_db(words) -> None:
    with db.begin() as session:
        session.bulk_save_objects(words)
        session.commit()


def get_all_chat_ids() -> int:
    """Генератор возвращающий id чата от каждого пользователя
    """
    with db.begin() as session:
        for id in session.query(models.User.chat_id).distinct():
            yield (id[0])
