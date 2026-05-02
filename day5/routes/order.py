from typing import List
from fastapi import APIRouter , Depends , HTTPException
from models.product_model import Order,OrderItems
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import getdb
from getuser import get_user
from models.product_model import Product

router = APIRouter()

class OrderItemsSchema(BaseModel):
    product_id: int
    quantity: int


class OrderSchema(BaseModel):
    items: List[OrderItemsSchema]


@router.post("/order")
def createorder(order: OrderSchema,db: Session = Depends(getdb),user: int = Depends(get_user)):
    try:
        neworder = Order(
            user_id = user
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
    result = []
    for o in orders:
        items = []
        for i in o.items:
            itm = db.query(Product).filter(Product.id == i.product_id).first()
            items.append({
                "product_name":itm.name,
                "quantity" : i.quantity
            })
        result.append({
            "order_id": o.id ,
            "user_id" : o.user_id,
            "items": items 
        })
    return result    