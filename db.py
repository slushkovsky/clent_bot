from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from config import DB_URI

Base = declarative_base() 

class User(Base): 
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True) 
    telegram_id = Column(Integer, unique=True) 
    chat_id = Column(Integer, unique=True) 

class Parser(Base): 
    __tablename__ = 'parsers'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User')  
    regex = Column(String)

class RSS(Base): 
    __tablename__ = 'rss'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User') 
    link = Column(String)
    last_upd_time = Column(DateTime, nullable=True) 

__engine = create_engine(DB_URI) 
Base.metadata.create_all(__engine)

Session = sessionmaker(bind=__engine)  
