from sqlalchemy import DateTime, Integer, Column, String, ForeignKey
from database import Base


class User(Base):
    __tablename__ = "USER"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    chat_id = Column(String)
    nick_name = Column(String)
    first_authorization = Column(String)


class Words(Base):
    __tablename__ = "LEARNED_WORDS"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("USER.name"), nullable=False)
    word = Column(String)
    time_stamp = Column(DateTime)
    message_id = Column(Integer)


class WordsStatus(Base):
    __tablename__ = "WORDS_STATUS"
    id = Column(Integer, primary_key=True)
    word_id = Column(Integer, ForeignKey("LEARNED_WORDS.id"), nullable=False)
    status = Column(Integer)
    time_stamp = Column(DateTime)