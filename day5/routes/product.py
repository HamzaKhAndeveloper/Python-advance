from fastapi import APIRouter , Depends , HTTPException
from models.product_model import Product
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import getdb

router = APIRouter()

class ProductSchema(BaseModel):
    name: str
    price: float 

@router.post("/product",status_code = 201)
def createproduct(product: ProductSchema, db: Session = Depends(getdb)):
    try:
        newproduct = Product(
        name = product.name,
        price = product.price
        )
        db.add(newproduct)
        db.commit()
        return {"message": "created successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code= 500,detail=f"server error : {str(e)}")

@router.get("/product",status_code=200)
def getproduct(db: Session = Depends(getdb)):
    products = db.query(Product).all()
    return products

@router.put("/product/{id}",status_code= 200)
def updateproduct(id: int,product: ProductSchema,db: Session = Depends(getdb)):
    updateproduct = db.query(Product).filter(Product.id == id).first()
    if updateproduct is None:
        raise HTTPException(status_code=404,detail="product not found")
    updateproduct.name = product.name
    updateproduct.price = product.price
    db.commit()
    return {"message": "update succefully"}

@router.delete("/product/{id}",status_code=200)
def delproduct(id: int,db: Session = Depends(getdb)):
    delproduct = db.query(Product).filter(Product.id == id).first()
    if delproduct is None:
        raise HTTPException(status_code=404,detail="product not found")
    db.delete(delproduct)
    db.commit()
    return {"message": "delete succefully"}

    
    