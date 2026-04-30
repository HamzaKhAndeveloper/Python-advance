from sqlalchemy.orm import relationship
from database import Base
from models.product import Product
from sqlalchemy import Column , Integer , String

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    products = relationship("Product",back_populates="user")