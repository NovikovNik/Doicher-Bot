from datetime import datetime
from database import get_db
import models

db = get_db()

def initial_user_create(user_name: str, nick: str, chat_id: id) -> None:
    new_user = models.User(name=user_name, 
                           first_authorization=datetime.now(), 
                           nick_name=nick, 
                           chat_id=chat_id)
    with db.begin() as session:
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
    
    
def find_user_in_db(user_id: int) -> models.User:
    with db.begin() as session:
        user = session.query(models.User).filter(models.User.name == user_id).first()
        return user


def delete_user_from_db(user_id: int) -> None:
    with db.begin() as session:
        session.query(models.User).filter(models.User.name == user_id).delete()
        session.commit()
        

def get_all_chat_ids() -> int:
    """Генератор возвращающий id чата от каждого пользователя
    """
    with db.begin() as session:
        for id in session.query(models.User.chat_id).distinct():
            yield(id[0])