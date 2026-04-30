from database import Base
from sqlalchemy import Column , Integer , String , Float ,ForeignKey
from sqlalchemy.orm import relationship


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    price = Column(Float)
    description = Column(String)
    user_id = Column(Integer,ForeignKey("users.id"))
    user = relationship("User",back_populates="product")
