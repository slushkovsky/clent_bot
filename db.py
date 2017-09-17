from sqlalchemy import create_engine, Column, Integer, String 
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from config import DB_URI

Base = declarative_base() 

class Parser(Base): 
    __tablename__ = 'parsers'

    id = Column(Integer, primary_key=True)
    user = Column(Integer)  
    regex = Column(String)

class RSS(Base): 
    __tablename__ = 'rss'

    id = Column(Integer, primary_key=True)
    user = Column(Integer) 
    link = Column(String)


__engine = create_engine(DB_URI) 
Base.metadata.create_all(__engine)

Session = sessionmaker(bind=__engine)  
