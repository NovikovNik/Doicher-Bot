from datetime import datetime
from database import get_db
import models

def initial_user_create(user_name, nick, chat_id):
    db = get_db()
    
    new_user = models.User(name=user_name, 
                           first_authorization=datetime.now(), 
                           nick_name=nick, 
                           chat_id=chat_id)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()
    
def find_user_in_db(user_id):
    db = get_db()
    
    user = db.query(models.User).filter(models.User.name == user_id).first()
    db.close()
    return user


def get_all_chat_ids():
        db = get_db()
        for id in db.query(models.User.chat_id).distinct():
            yield(id[0])