from sqlalchemy import Integer, Column, String, ForeignKey, Date
from database import Base


class User(Base):
    __tablename__ = "USER"
    id = Column(Integer, primary_key = True)
    name = Column(String)
    chat_id = Column(String)
    nick_name = Column(String)
    first_authorization = Column(String)
    
class Words(Base):
    __tablename__ = "LEARNED_WORDS"
    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey("USER.id"), nullable=False)
    word = Column(String)
    time_stamp = Column(Date)
    