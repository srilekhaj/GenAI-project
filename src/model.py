from sqlalchemy import Column, Boolean, Integer, String, Float
from database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50))
    account_number = Column(String(50), unique=True, index=True)
    balance = Column(Float, default=0)

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50))
    content = Column(String(50))
    user_id = Column(Integer)


#CREATE TABLE users(id primary key, username varchar(50), account_number varchar(50), balance float);


