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


def add_user(user) -> None:
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


def add_new_word_to_db(chat_id: int, word: str, message_id: int) -> None:
    with db.begin() as session:
        name = session.query(models.User.name).filter(
            models.User.chat_id == chat_id).first()
        new_word = models.Words(
            user_id=name[0], word=word, time_stamp=datetime.now(), message_id = message_id)
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


def set_word_status(id, status) -> None:
    """добавление в таблицу WORDS_STATUS. Id слова берется по id сообщения -1. Тут костыль,
    но я пока не понял в чем дело
    """
    with db.begin() as session:
        print(f"id: {id}")
        word_id = session.query(models.Words.id).filter(
            models.Words.message_id == id-1).first()
        print(f"word_id: {word_id}")
        new_status = models.WordsStatus(
            word_id=word_id[0], status=status, time_stamp=datetime.now())
        session.add(new_status)
        session.commit()
        