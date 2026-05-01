from sqlalchemy import Column , Integer , String , Float,ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Product(Base):
    __tablename__ = "product_d5"
    id = Column(Integer, primary_key = True,index = True)
    name = Column(String)
    price = Column(Float)


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key = True , index = True)
    user_id = Column(Integer,ForeignKey("users_d5.id"))
    items = relationship("OrderItems", back_populates = "order")

class OrderItems(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key = True , index = True)
    order_id =  Column(Integer , ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("product_d5.id"))
    quantity = Column(Integer,default = 1)
    order =  relationship("Order",back_populates = "items")
