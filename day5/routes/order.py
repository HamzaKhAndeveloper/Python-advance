from typing import List
from fastapi import APIRouter , Depends , HTTPException
from models.product_model import Order,OrderItems
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import getdb


router = APIRouter()

class OrderSchema(BaseModel):
    user_id: int 
    items: List[OrderItemsSchema]

class OrderItemsSchema(BaseModel):
    order_id: int
    product_id: int
    quantity: int

@router.post("/order")
def createorder(order: OrderSchema,db: Session = Depends(getdb)):
    try:
        neworder = Order(
            user_id = order.user_id
        )
        db.add(neworder)
        db.flush()

        for p in order.items:
            newitem = OrderItems(
                order_id = neworder.id,
                product_id = p.product_id,
                quantity = p.quantity
            )
            db.add(newitem)
        db.commit()
        return {"message": "created successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code= 500,detail=f"server error : {str(e)}")


@router.get("/order",status_code=200)
def getorders(db: Session = Depends(getdb)):
    orders = db.query(Order).all()
    return orders