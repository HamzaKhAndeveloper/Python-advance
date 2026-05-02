from sqlalchemy import Column, Integer , String 
from database import Base


class User(Base):
    __tablename__ = "users_d5"
    id = Column(Integer,primary_key = True,index = True)
    name = Column(String(100))
    email = Column(String(100))
    password = Column(String(255))