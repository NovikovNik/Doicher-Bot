from datetime import datetime, timedelta
from database import get_db
import models
import re
from dataclasses import dataclass

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
            user_id=name[0], word=word, time_stamp=datetime.now(), message_id=message_id)
        session.add(new_word)
        session.commit()
        # session.refresh(new_word)


def create_word_object(chat_id: int, word: str, message_id: int):
    return models.Words(user_id=chat_id, word=word, time_stamp=datetime.now(), message_id=message_id)


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
    """добавление в таблицу WORDS_STATUS """
    with db.begin() as session:
        print(f"id: {id}")
        word_id = session.query(models.Words.id).filter(
            models.Words.message_id == id).first()
        print(f"word_id: {word_id}")
        new_status = models.WordsStatus(
            word_id=word_id[0], status=status, time_stamp=datetime.now())
        session.add(new_status)
        session.commit()


@dataclass
class Data():
    know_words = 'know_words'
    unknown_words = 'unknow_words'
    all_words = 'all_words'
    since = 'since'
    last_week = 'last_week'


def get_user_stats(user_id: int, week=False) -> dict:
    with db.begin() as session:
        if week == False:
            result = {Data.all_words: session.query(models.Words).filter(models.Words.user_id == user_id).count(),
                      Data.know_words: session.query(models.Words, models.WordsStatus)
                      .filter(models.Words.user_id == user_id)
                      .filter(models.WordsStatus.status == 1)
                      .filter(models.WordsStatus.word_id == models.Words.id).distinct().count(),
                      Data.unknown_words: session.query(models.Words, models.WordsStatus)
                      .filter(models.Words.user_id == user_id)
                      .filter(models.WordsStatus.status == 0)
                      .filter(models.WordsStatus.word_id == models.Words.id).distinct().count(),
                      Data.since: re.escape(str(session.query(models.User.first_authorization)
                                   .filter(models.User.name == user_id).first()).strip("('").split(' ')[0])}
        else:
            result = {Data.all_words: session.query(models.Words)
                      .filter(models.Words.user_id == user_id)
                      .filter(models.Words.time_stamp >= (datetime.now() - timedelta(weeks=1))).count(),
                      Data.know_words: session.query(models.Words, models.WordsStatus)
                      .filter(models.Words.user_id == user_id)
                      .filter(models.Words.time_stamp >= (datetime.now() - timedelta(weeks=1)))
                      .filter(models.WordsStatus.status == 1)
                      .filter(models.WordsStatus.word_id == models.Words.id).distinct().count(),
                      Data.unknown_words: session.query(models.Words, models.WordsStatus)
                      .filter(models.Words.user_id == user_id)
                      .filter(models.Words.time_stamp >= (datetime.now() - timedelta(weeks=1)))
                      .filter(models.WordsStatus.status == 0)
                      .filter(models.WordsStatus.word_id == models.Words.id).distinct().count(),
                      Data.since: re.escape(str(session.query(models.User.first_authorization)
                                   .filter(models.User.name == user_id).first()).strip("('").split(' ')[0]),
                      Data.last_week: re.escape((datetime.now() - timedelta(weeks=1)).strftime("%Y-%d-%m"))
                      }
            
        return result
