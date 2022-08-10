from datetime import datetime
from database import get_db
import models

def initial_user_create(user_name: str, nick: str, chat_id: id):
    db = get_db()
    new_user = models.User(name=user_name, 
                           first_authorization=datetime.now(), 
                           nick_name=nick, 
                           chat_id=chat_id)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()
    
def find_user_in_db(user_id: int) -> models.User:
    db = get_db()
    user = db.query(models.User).filter(models.User.name == user_id).first()
    db.close()
    return user


def delete_user_from_db(user_id: int) -> None:
    db = get_db()
    db.query(models.User).filter(models.User.name == user_id).delete()
    db.commit()
    db.close()

def get_all_chat_ids() -> int:
    """Генератор возвращающий id чата от каждого пользователя
    """
    db = get_db()
    for id in db.query(models.User.chat_id).distinct():
        yield(id[0])