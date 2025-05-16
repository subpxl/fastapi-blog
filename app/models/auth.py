from sqlalchemy import Column,DateTime,Integer,String,Enum,create_engine
from datetime import datetime
from database import Base


class User(Base):
    __tablename__="user"
    id =Column(Integer,primary_key=True,index=True)
    username=Column(String,unique=True,index=True)
    email=Column(String,unique=True,index=True)
    password_hash = Column(String)
    created_at = Column(DateTime,default=datetime.now)